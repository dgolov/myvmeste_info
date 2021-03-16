from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Max, Min
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from profiles.forms import FeedBackForm
from profiles.models import ReferralCodes, FeedBackRequests
from profiles.views import FEEDBACK_MESSAGE_TEMPLATE
from .models import DebitCards, CreditCards, Categories, PotrebCredits, Mortgages, MFO, RKO, Refinancing
from .mixins import CategoryDetailMixin, UserMixin, CT_MODEL_MODEL_CLASS
from urllib.parse import urlparse


class MainView(UserMixin, View):
    """ Представление главной страницы
    """
    def get(self, request, *args, **kwargs):
        if self.user.is_anonymous:
            try:
                ref_code = request.GET.get('r', '')
                referral = ReferralCodes.objects.get(code=ref_code)
                request.session['referral'] = referral.user.username
                return HttpResponseRedirect('/profile/signup')
            except:
                pass
        context = {'user': self.user, 'referred_user': self.referred_user, 'title': "Мы вместе"}
        return render(request, 'web/index.html', context)


class OffersView(UserMixin, ListView):
    """ Представление раздела категорий офферов
    """
    model = Categories
    template_name = 'web/all_offers.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OffersView, self).get_context_data()
        context['title'] = 'Офферы'
        context['user'] = self.user
        context['referred_user'] = self.referred_user
        context['debit_cards'] = DebitCards.objects.filter(is_active=True).aggregate(Max('reward'), Max('cash_back'))
        context['credit_cards'] = CreditCards.objects.filter(is_active=True).aggregate(Max('reward'), Max('limit'))
        context['credits'] = PotrebCredits.objects.filter(is_active=True).aggregate(Max('reward'), Min('percents'))
        context['ipoteka'] = Mortgages.objects.filter(is_active=True).aggregate(Max('reward'), Min('percents'))
        context['rko'] = RKO.objects.filter(is_active=True).aggregate(Max('reward'), Min('service_cost'))
        context['refenancing'] = Refinancing.objects.filter(is_active=True).aggregate(Max('reward'), Min('percents'))
        context['mfo'] = MFO.objects.filter(is_active=True).aggregate(Max('reward'), Min('percents'))
        return context

    def get_queryset(self):
        return Categories.objects.filter(is_active=True).order_by('name')


class CategoryDetailView(UserMixin, CategoryDetailMixin, DetailView):
    """ Представление раздела конкретной категории офферов
    """
    model = Categories
    queryset = Categories.objects.all()
    context_object_name = 'category'
    template_name = 'web/offers.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        context['referred_user'] = self.referred_user
        return context


# class OffersDetailView(UserMixin, CategoryMixin, DetailView):
#     """ Представление раздела конкретного оффера
#     """
#     context_object_name = 'product'
#     template_name = 'web/offers_detail.html'
#     slug_url_kwarg = 'slug'
#
#     def dispatch(self, request, *args, **kwargs):
#         self.model = CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
#         self.queryset = self.model._base_manager.all()
#         return super().dispatch(request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['ct_model'] = self.model._meta.model_name
#         context['category'] = Categories.objects.order_by('name')
#         context['user'] = self.user
#         context['categories'] = self.categories
#         return context


class OffersRedirectView(UserMixin, View):
    """ Редирект на страницу банка при нажатии кнопки "Оформить заявку"
    """
    def dispatch(self, request, *args, **kwargs):
        self.model = CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.offer = self.model.objects.get(id=kwargs['product_id'])
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        url = None
        domain = urlparse(self.offer.referral_slug).netloc
        if domain == 'pxl.leads.su':
            url = '{}?aff_sub1={}'
        elif domain == 'gl.guruleads.ru':
            url = '{}?sub1={}'
        if self.user.profile.struct == 1 and url:
            url = url.format(self.offer.referral_slug, self.user.profile.pk)
            # message = f'Переход по ссылке на {self.offer}'
            # add_to_user_history_list(self.user, message)
        elif self.user.profile.struct == 2 and url:
            url = url.format(self.offer.referral_slug_2, self.user.profile.pk)
        else:
            url = self.offer.referral_slug
        return HttpResponseRedirect(url)


class RegulationsView(UserMixin, View):
    """ Представление раздела правила программы
    """
    def get(self, request, *args, **kwargs):
        context = {
                'user': self.user,
                'title': "Правила программы",
                'referred_user': self.referred_user,
        }
        return render(request, 'web/regulations.html', context)


class ImportantAsView(UserMixin, View):
    """ Представление раздела FAQ
    """
    def get(self, request, *args, **kwargs):
        context = {
            'user': self.user,
            'title': "Важно знать",
            'referred_user': self.referred_user,
        }
        return render(request, 'web/important.html', context)


class FAQAsView(UserMixin, View):
    """ Представление раздела FAQ
    """
    def get(self, request, *args, **kwargs):
        context = {
            'user': self.user,
            'title': "FAQ",
            'referred_user': self.referred_user,
        }
        return render(request, 'web/faq.html', context)


class AboutAsView(CreateView, UserMixin, View):
    form_class = FeedBackForm
    template_name = 'web/about.html'
    """ Представление раздела контакты
    """
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
        context = super(AboutAsView, self).get_context_data()
        context['user'] = self.user
        context['title'] = 'О проекте'
        context['referred_user'] = self.referred_user
        return context


class SearchView(UserMixin, ListView):
    """ Поиск
    """
    template_name = 'web/search.html'
    context_object_name = 'debit_cards'
    context_names = ['debit_cards', 'credit_cards', 'credits', 'rko', 'refinancing', 'mfo', 'ipoteka']

    def get_queryset(self):
        search_text = self.request.GET.get('search')
        return DebitCards.objects.filter(card_name__icontains=search_text)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        success = False
        search_text = self.request.GET.get('search')
        context['user'] = self.user
        context['referred_user'] = self.referred_user
        context['credit_cards'] = CreditCards.objects.filter(card_name__icontains=search_text)
        context['credits'] = PotrebCredits.objects.filter(bank_name__icontains=search_text)
        context['rko'] = RKO.objects.filter(bank_name__icontains=search_text)
        context['refinancing'] = Refinancing.objects.filter(bank_name__icontains=search_text)
        context['mfo'] = MFO.objects.filter(bank_name__icontains=search_text)
        context['ipoteka'] = Mortgages.objects.filter(bank_name__icontains=search_text)
        context['title'] = 'Поиск'
        for name in self.context_names:
            if len(context[name]) > 0:
                print(len(context[name]))
                success = True
                break
        if not success:
            context['none'] = 'По вашему запросу ничего не найдено'
        return context