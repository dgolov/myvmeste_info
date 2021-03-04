from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, CreateView
from .forms import *
from .models import Profile, ApplicationsForMoney, Cards, History, FeedBackRequests
from .mixins import ProfileMixin
from .utils import get_referred_user, create_referral_struct
import xlwt
from datetime import datetime


FEEDBACK_MESSAGE_TEMPLATE = '''Категория сообщения: "{}"

Пользователь {}, 
телефон: {}
E-mail: {}

Тема сообщения: {}

Сообщение:
{}'''


class ProfileView(ProfileMixin, View):
    """ Представление страницы личного кабинета
    """
    def __init__(self):
        super(ProfileView, self).__init__()
        self.context['title'] = 'Личный кабинет'

    def get(self, request, *args, **kwargs):
        self.get_context_data(request)
        return render(request, 'profiles/profile.html', self.context)

    def post(self, request, *args, **kwargs):
        super(ProfileView, self).post(request, *args, **kwargs)
        self.get_context_data(request)
        return render(request, 'profiles/profile.html', self.context)

    def get_context_data(self, request):
        super(ProfileView, self).get_context_data(request)
        self.context['struct1'] = self.user.profile.struct1.all().select_related('profile', 'profile__referred')
        self.context['struct2'] = self.user.profile.struct2.all().select_related('profile', 'profile__referred')
        self.context['struct3'] = self.user.profile.struct3.all().select_related('profile', 'profile__referred')
        self.context['struct4'] = self.user.profile.struct4.all().select_related('profile', 'profile__referred')
        self.context['struct5'] = self.user.profile.struct5.all().select_related('profile', 'profile__referred')


class RegisterView(View):
    """ Представление раздела регистрации
    """
    def __init__(self):
        super(RegisterView, self).__init__()
        self.message = '''Уважаемый(ая) {}

        Вы успешно зарегестрировались в проекте myvmeste.info
        Для того чтобы начать зарабатывать на нашей площадке необходимо:
        - Оформить любой банковский продукт в разделе "Офферы"
        - Получить реферальную ссылку в разделе "Личный кабинет"
        - Пригласить новых участников в свою первую линию

        Желаем Вам успехов!

                С уважением, администрация МыВместе!
        '''

    def get(self, request, *args, **kwargs):
        referred_user = get_referred_user(request)
        if request.user.is_authenticated:
            return HttpResponseRedirect('/profile')
        if referred_user is not None:
            user_form = UserRegistrationForm()
            context = {'title': "Регистрация", 'referred_user': referred_user, 'form': user_form}
            return render(request, 'profiles/singup.html', context)
        else:
            raise Http404("Poll does not exist")

    def post(self, request, *args, **kwargs):
        referred_user = get_referred_user(request)
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            new_user.profile.phone = user_form.cleaned_data['phone']
            new_user.profile.location = user_form.cleaned_data['location']
            new_user.save()
            if referred_user:
                new_user.profile.referred = referred_user
                new_user.profile.struct = referred_user.profile.struct
                new_user.save()
                create_referral_struct(referred_user, new_user, 1)
            send_mail(
                'Регистрация в проекте "МыВместе"',
                self.message.format(new_user.get_full_name()),
                'mail@myvmeste.info',
                ['{}'.format(new_user.email)],
                fail_silently=False
            )
            messages.add_message(request, messages.INFO, 'Вы успешно зарегестрировались')
            login(request, new_user)
            return HttpResponseRedirect('/')
        context = {'title': "Регистрация", 'referred_user': referred_user, 'form': user_form}
        return render(request, 'profiles/singup.html', context)


class SettingsView(ProfileMixin, View):
    """ Представление раздела настроек
    """
    def __init__(self):
        super(SettingsView, self).__init__()
        user_settings_form = UserSettingsForm()
        add_card_form = AddCardsForm()
        self.context['settings_form'] = user_settings_form
        self.context['card_form'] = add_card_form
        self.context['title'] = 'Настройки профиля'

    def get(self, request, *args, **kwargs):
        self.get_context_data(request)
        return render(request, 'profiles/settings.html', self.context)

    def post(self, request, *args, **kwargs):
        super(SettingsView, self).post(request, *args, **kwargs)
        user_form = UserSettingsForm(request.POST)
        add_card_form = AddCardsForm(request.POST)
        self.get_context_data(request)

        if 'card' in request.POST:
            if add_card_form.is_valid():
                card_number = int(add_card_form.cleaned_data['card'])
                Cards.objects.create(card=card_number, user=request.user)
                messages.add_message(request, messages.INFO, 'Карта добавлена успешно')
            else:
                messages.add_message(request, messages.ERROR, 'Ошибка добавления карты')

        if 'first_name' in request.POST or 'last_name' in request.POST or 'location' in request.POST:
            if user_form.is_valid():
                first_name = user_form.cleaned_data['first_name']
                if first_name:
                    request.user.first_name = first_name
                last_name = user_form.cleaned_data['last_name']
                if last_name:
                    request.user.last_name = last_name
                location = user_form.cleaned_data['location']
                if location:
                    request.user.profile.location = location
                if first_name or last_name or location:
                    request.user.save()
                    messages.add_message(request, messages.INFO, 'Изменения внесены успешно')
        if 'email' in request.POST:
            if user_form.is_valid():
                email = user_form.cleaned_data['email']
                if email:
                    request.user.email = email
                    request.user.save()
                    messages.add_message(request, messages.INFO, 'Ваш email успешно изменен')
            else:
                messages.add_message(request, messages.ERROR, 'Пользователь с таким email уже существует.')
        return render(request, 'profiles/settings.html', self.context)


class DeleteCard(ProfileMixin, View):
    """ Удаление карты пользователем
    """
    raise_exception = True

    def get(self, request, *args, **kwargs):
        self.get_context_data(request)
        try:
            pk = kwargs.get('pk')
            card = Cards.objects.get(pk=pk)
        except Cards.DoesNotExist:
            return HttpResponseRedirect('/profile/settings')
        if request.user == card.user:
            card.delete()
            messages.add_message(request, messages.INFO, 'Карта успешно удалена')
        return HttpResponseRedirect('/profile/settings')


class GetApplicationsReport(View):
    """ Загрузка отчета с заявками на выплату денежных средств
    """
    def get(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("Poll does not exist")
        applications = ApplicationsForMoney.objects.filter(is_processed=False)
        cols = {
            0: 'ID Запроса',
            1: 'ID Партнера',
            2: 'Партнер',
            3: 'Запрошенная сумма',
            4: 'Дата запроса',
            5: 'Номер карты',
            6: 'Выплачено',
        }
        sizes = {0: 3000, 1: 3500, 2: 8000, 3: 5300, 4: 4500, 5: 5300, 6: 3500}
        report = xlwt.Workbook()
        sheet1 = report.add_sheet("Запросы на вывод")
        style = xlwt.easyxf('font: bold 1;')
        for num in range(7):
            sheet1.col(num).width = sizes[num]

        row = sheet1.row(0)
        num = 2
        for key, value in cols.items():
            row.write(key, value, style)

        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        style = xlwt.XFStyle()
        style.alignment = alignment
        for application in applications:
            user = application.user
            row = sheet1.row(num)
            row.write(0, application.id, style)
            row.write(1, application.user.id, style)
            row.write(2, application.user.get_full_name(), style)
            row.write(3, application.reserved, style)
            row.write(4, application.created_at.strftime("%d-%m-%Y %H:%M"), style)
            row.write(5, application.card, style)
            text = 'Да' if application.is_paid_out else 'Нет'
            row.write(6, text, style)
            # Заявка обработана
            application.is_processed = True
            money = user.profile.balance.reserved
            user.profile.balance.reserved -= money
            user.profile.balance.accrued += money
            user.profile.balance.save()
            application.save()
            num += 1
        date = datetime.now()

        report.save("media/downloads/report{}.xls".format(date.strftime("%Y%m%d%H%M")))
        return HttpResponseRedirect('/media/downloads/report{}.xls'.format(date.strftime("%Y%m%d%H%M")))


class MessagesView(ListView, ProfileMixin):
    model = History
    template_name = 'profiles/messages_list.html'
    context_object_name = 'messages'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        context['title'] = 'Сообщения'
        context['application_form'] = ApplicationsForMoneyForm()
        context['order_form'] = UploadFileForm()
        context['order_form_pay'] = UploadOrderPayForm()
        return context

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-id')

    def post(self, request, *args, **kwargs):
        super(MessagesView, self).post(request, *args, **kwargs)
        return HttpResponseRedirect('/profile/messages')


class FeedbackView(CreateView, ProfileMixin):
    form_class = FeedBackForm
    template_name = 'profiles/feedback.html'

    def post(self, request, *args, **kwargs):
        self.form_class = FeedBackForm(request.POST)
        if self.form_class.is_valid():
            question_category = request.POST['question_category']
            feed_back = FeedBackRequests.objects.create(**self.form_class.cleaned_data, user=self.request.user)
            send_mail(
                'Сообщение обратной связи "МыВместе"',
                FEEDBACK_MESSAGE_TEMPLATE.format(
                    question_category,
                    feed_back.user.get_full_name(),
                    feed_back.user.email,
                    feed_back.user.profile.phone,
                    feed_back.theme,
                    feed_back.message
                    ),
                'mail@myvmeste.info', ['dgolov@icloud.com'], fail_silently=False
                )
            messages.add_message(request, messages.INFO, 'Ваше сообщение успешно отправлено')
        else:
            messages.add_message(request, messages.ERROR, 'Ваше сообщение не было отправлено')
        return HttpResponseRedirect('/profile')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FeedbackView, self).get_context_data()
        add_card_form = AddCardsForm()
        context['card_form'] = add_card_form
        context['title'] = 'Обратная связь'
        return context


class ChangePhoneView(LoginRequiredMixin, View):
    """ Представление страницы редактирования номера телефона
    """
    login_url = '/profile/login'

    def get(self, request, *args, **kwargs):
        change_phone_form = ChangePhoneForm()
        context = {'form': change_phone_form, 'title': 'Изменить номер телефона'}
        return render(request, 'profiles/change-phone.html', context)

    def post(self, request, *args, **kwargs):
        change_phone_form = ChangePhoneForm(request.POST)
        if change_phone_form.is_valid():
            profile = Profile.objects.get(user=request.user)
            phone = change_phone_form.cleaned_data['phone']
            profile.phone = phone
            profile.save()
            messages.add_message(request, messages.INFO, f'Номер телефона успешно изменен.')
        else:
            messages.add_message(request, messages.ERROR, f'Указанный номер телефона уже зарегистрирован в системе.')
        return HttpResponseRedirect('/profile/settings')