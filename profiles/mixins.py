from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from .models import Profile, Orders, ApplicationsForMoney, Cards
from .forms import ApplicationsForMoneyForm, UploadFileForm, UploadOrderPayForm
from .utils import get_product
from web.mixins import money_distribution
from web.models import IDOrders, Offers
from openpyxl import load_workbook


class ProfileMixin(LoginRequiredMixin, View):
    login_url = '/profile/login'

    def __init__(self):
        super(ProfileMixin, self).__init__()
        self.application_form = ApplicationsForMoneyForm()
        self.order_form = UploadFileForm()
        self.order_form_pay = UploadOrderPayForm()
        self.user = None
        self.context = {
            'application_form': self.application_form,
            'order_form': self.order_form,
            'order_form_pay': self.order_form_pay,
        }

    def post(self, request, *args, **kwargs):
        if 'report' in request.FILES:
            self.download_report(request)
        if 'report_pay' in request.FILES:
            self.download_report_pay(request)
        if 'reserved' in request.POST:
            application_form = ApplicationsForMoneyForm(request.POST)
            card = request.POST['card']
            user = request.user
            if application_form.is_valid():
                reserved = application_form.cleaned_data['reserved']
            else:
                reserved = None
            balance = user.profile.available()
            if reserved and balance >= reserved:
                user.profile.balance.available -= reserved
                if user.profile.balance.available < 0:
                    difference = user.profile.balance.available
                    user.profile.balance.self_available += difference
                    user.profile.balance.available = 0
                user.profile.balance.reserved += reserved
                ApplicationsForMoney.objects.create(user=user, card=card, reserved=reserved)
                user.profile.balance.save()
                messages.add_message(
                    request,
                    messages.INFO,
                    '{} руб зарезервированы для вывода и будут выплачены в течении 7 дней'.format(reserved))
            else:
                messages.add_message(request, messages.ERROR, 'Ошибка вывода денежных средств')

    def get_context_data(self, request):
        self.user = request.user
        cards = Cards.objects.filter(user=self.user).select_related('user')
        self.context['cards'] = cards
        self.context['user'] = self.user

    def download_report(self, request):
        """ Загрузка отчета партнерки
        """
        item_row, item_user, money = 0, 0, 0
        order_id, offer_id = None, None
        self.order_form = UploadFileForm(request.POST, request.FILES)
        order = IDOrders()
        new_upload_order = Orders()

        if self.order_form.is_valid():
            new_upload_order.order = request.FILES['report']
            new_upload_order.save()
            ex_data = load_workbook('./media/uploads/{}'.format(request.FILES['report']))
            first_sheet = ex_data.get_sheet_names()[0]
            worksheet = ex_data.get_sheet_by_name(first_sheet)
            confirmed = {}

            for row in worksheet.iter_rows():
                new_order = False
                item_row += 1
                if item_row == 1:
                    continue
                item_col = 0
                for cell in row:
                    item_col += 1
                    if item_col == 1:
                        try:
                            order = IDOrders.objects.get(order_id=cell.value)
                        except IDOrders.DoesNotExist:
                            order_id = cell.value
                            new_order = True
                    elif item_col == 3:
                        offer_id = int(cell.value.split(',')[0])
                        money = Offers.objects.get(offer_id=offer_id)
                    elif item_col == 6:
                        item_user = Profile.objects.get(id=int(cell.value))
                    elif item_col == 11:
                        if not new_order and order.status != cell.value:
                            # Отчет уже есть, но статус изменен
                            confirmed[item_user] = cell.value
                            order.status = cell.value
                            order.save()
                            first_user = {'user': item_user.user.get_full_name(), 'offer': get_product(order)}
                            money_distribution(marketing_money=money.reward, rest_of_money=money.reward,
                                               first_user=first_user, item_user=item_user.user,
                                               level_struct=0, order=order)
                        elif new_order:
                            # Отчета нет в системе, создание нового
                            confirmed[item_user] = cell.value
                            order = IDOrders.objects.create(
                                user=item_user,
                                order_id=order_id,
                                offer_id=offer_id,
                                status=cell.value,
                                broker=item_user.broker,
                            )
                            first_user = {'user': item_user.user.get_full_name(), 'offer': get_product(order)}
                            money_distribution(marketing_money=money.reward, rest_of_money=money.reward,
                                               first_user=first_user, item_user=item_user.user,
                                               level_struct=0, order=order, new_order=True)
            new_upload_order.delete()

            # Присвоение статуса брокера для пользователей с подтвержденными заявками
            for user, status in confirmed.items():
                if status == 'Подтвержден':
                    user.broker = True
                    user.save()

    def download_report_pay(self, request):
        """ Загрузка отчета выплаченных средств
        """
        item_row = 0
        item_application = None
        item_balance = None
        item_user = None
        new_upload_order = Orders()
        self.order_form_pay = UploadOrderPayForm(request.POST, request.FILES)

        if self.order_form_pay.is_valid():
            new_upload_order.order = request.FILES['report_pay']
            new_upload_order.save()
            ex_data = load_workbook('./media/uploads/{}'.format(request.FILES['report_pay']))
            first_sheet = ex_data.get_sheet_names()[0]
            worksheet = ex_data.get_sheet_by_name(first_sheet)

            for row in worksheet.iter_rows():
                item_row += 1
                if item_row == 1 or item_row == 2:
                    continue
                item_col = 0
                for cell in row:
                    item_col += 1
                    if item_col == 1:
                        item_application = ApplicationsForMoney.objects.get(pk=cell.value)
                        item_user = item_application.user.profile
                        item_balance = item_user.balance
                    elif item_col == 7:
                        status = cell.value
                        if status == 'Да' or status == 'да' or status == '1':
                            money = item_application.reserved
                            item_balance.accrued -= money
                            item_balance.paid_out += money
                            item_balance.save()
                            item_application.is_paid_out = True
                            item_application.save()
            new_upload_order.delete()
