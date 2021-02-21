from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from api.serializers import UserSerializer, CategorySerializer, CreditCardsSerializer, DebitCardsSerializer, \
    PotrebCreditsSerializer, RefinancingSerializer, MortgagesSerializer, MFOSerializer, RKOSerializer
from web.models import Categories, CreditCards, DebitCards, PotrebCredits, Refinancing, Mortgages, MFO, RKO


class UserViewSet(viewsets.ModelViewSet):
    """ Представление API User
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryListApiView(ListAPIView):
    """ Представление API Категорий
    """
    serializer_class = CategorySerializer
    queryset = Categories.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CreditCardsApiView(ListAPIView):
    """ Представление API Кредитных карт
    """
    serializer_class = CreditCardsSerializer
    queryset = CreditCards.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['card_name', 'bank_name', 'reward']


class CreditCardsDetailApiView(RetrieveAPIView):
    """ Представление API конкретной кредитной карты
    """
    serializer_class = CreditCardsSerializer
    queryset = CreditCards.objects.filter(is_active=True)
    lookup_field = 'slug'


class DebitCardsApiView(ListAPIView):
    """ Представление API Дебетовых карт
    """
    serializer_class = DebitCardsSerializer
    queryset = DebitCards.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['card_name', 'bank_name', 'reward']


class DebitCardsDetailApiView(RetrieveAPIView):
    """ Представление API конкретной дебетовой карты
    """
    serializer_class = DebitCardsSerializer
    queryset = DebitCards.objects.filter(is_active=True)
    lookup_field = 'slug'


class PotrebCreditsApiView(ListAPIView):
    """ Представление API Потребительских кредитов
    """
    serializer_class = PotrebCreditsSerializer
    queryset = PotrebCredits.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['bank_name', 'reward']


class PotrebCreditsDetailApiView(RetrieveAPIView):
    """ Представление API конкретного потребительского кредита
    """
    serializer_class = PotrebCreditsSerializer
    queryset = PotrebCredits.objects.filter(is_active=True)
    lookup_field = 'slug'


class RefinancingApiView(ListAPIView):
    """ Представление API Рефенансирования
    """
    serializer_class = RefinancingSerializer
    queryset = Refinancing.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['bank_name', 'reward']


class RefinancingDetailApiView(RetrieveAPIView):
    """ Представление API конкретного кредита рефенансирования
    """
    serializer_class = RefinancingSerializer
    queryset = Refinancing.objects.filter(is_active=True)
    lookup_field = 'slug'


class MortgagesApiView(ListAPIView):
    """ Представление API Ипотеки
    """
    serializer_class = MortgagesSerializer
    queryset = Mortgages.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['bank_name', 'reward']


class MortgagesDetailApiView(RetrieveAPIView):
    """ Представление API конкретного ипотечного кредита
    """
    serializer_class = MortgagesSerializer
    queryset = Mortgages.objects.filter(is_active=True)
    lookup_field = 'slug'


class MFOApiView(ListAPIView):
    """ Представление API МФО
    """
    serializer_class = MFOSerializer
    queryset = MFO.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['bank_name', 'reward']


class MFODetailApiView(RetrieveAPIView):
    """ Представление API конкретного МФО
    """
    serializer_class = MFOSerializer
    queryset = MFO.objects.filter(is_active=True)
    lookup_field = 'slug'


class RKOApiView(ListAPIView):
    """ Представление API РКО
    """
    serializer_class = RKOSerializer
    queryset = RKO.objects.filter(is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ['bank_name', 'reward']


class RKODetailApiView(RetrieveAPIView):
    """ Представление API конкретного РКО
    """
    serializer_class = RKOSerializer
    queryset = RKO.objects.filter(is_active=True)
    lookup_field = 'slug'