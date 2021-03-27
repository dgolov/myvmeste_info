from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Categories, DebitCards, CreditCards, PotrebCredits, MFO, Mortgages, RKO, Refinancing
from profiles.utils import get_referred_user


# Content Types моделей офферов
CT_MODEL_MODEL_CLASS = {
        'debetovye-karty': DebitCards,
        'kreditnye-karty': CreditCards,
        'mfo': MFO,
        'potrebitelskie-kredity': PotrebCredits,
        'ipotechnye-kredity': Mortgages,
        'rasschetno-kassovoe-oborudovanie': RKO,
        'refenansirovanie': Refinancing,
    }


class UserMixin(View):

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.referred_user = get_referred_user(request)
        return super().dispatch(request, *args, **kwargs)


class CategoryDetailMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Categories):
            model = CT_MODEL_MODEL_CLASS[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['products'] = model.objects.filter(is_active=True).select_related('category')
            return context

        context = super().get_context_data(**kwargs)
        return context
