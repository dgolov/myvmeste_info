from rest_framework import routers
from api.api_views import UserViewSet
from django.urls import path, include
from .api_views import (
    CategoryListApiView, CreditCardsApiView, DebitCardsApiView, PotrebCreditsApiView, MortgagesApiView,
    RefinancingApiView, MFOApiView, RKOApiView, CreditCardsDetailApiView, DebitCardsDetailApiView,
    PotrebCreditsDetailApiView, MortgagesDetailApiView, RefinancingDetailApiView, MFODetailApiView, RKODetailApiView
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('offers/', CategoryListApiView.as_view()),
    path('offers/kreditnye-karty/', CreditCardsApiView.as_view()),
    path('offers/kreditnye-karty/<str:slug>/', CreditCardsDetailApiView.as_view()),
    path('offers/debetovye-karty/', DebitCardsApiView.as_view()),
    path('offers/debetovye-karty/<str:slug>/', DebitCardsDetailApiView.as_view()),
    path('offers/potrebitelskie-kredity/', PotrebCreditsApiView.as_view()),
    path('offers/potrebitelskie-kredity/<str:slug>/', PotrebCreditsDetailApiView.as_view()),
    path('offers/ipotechnye-kredity/', MortgagesApiView.as_view()),
    path('offers/ipotechnye-kredity/<str:slug>/', MortgagesDetailApiView.as_view()),
    path('offers/refenansirovanie/', RefinancingApiView.as_view()),
    path('offers/refenansirovanie/<str:slug>/', RefinancingDetailApiView.as_view()),
    path('offers/mfo/', MFOApiView.as_view()),
    path('offers/mfo/<str:slug>/', MFODetailApiView.as_view()),
    path('offers/rasschetno-kassovoe-oborudovanie/', RKOApiView.as_view()),
    path('offers/rasschetno-kassovoe-oborudovanie/<str:slug>/', RKODetailApiView.as_view()),
]
