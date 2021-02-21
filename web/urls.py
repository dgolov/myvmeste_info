from django.urls import path
from django.views.decorators.cache import cache_page
from .views import MainView, CategoryDetailView, FAQAsView, RegulationsView, OffersView, AboutAsView, \
    OffersRedirectView, SearchView, ImportantAsView


urlpatterns = [
    path('', cache_page(60)(MainView.as_view()), name='home'),
    path('offers/', cache_page(60)(OffersView.as_view()), name='offers'),
    path('offers/<str:slug>/', cache_page(60)(CategoryDetailView.as_view()), name='category_detail'),
    path('regulations', RegulationsView.as_view(), name='regulations'),
    path('regulations/important', ImportantAsView.as_view(), name='important'),
    path('contacts', AboutAsView.as_view(), name='contacts'),
    path('faq', FAQAsView.as_view(), name='faq'),
    path('offer-redirect/<str:ct_model>/<int:product_id>', OffersRedirectView.as_view(), name='redirect_offer'),
    path('search/', SearchView.as_view(), name='search'),
]

# path('offers/<str:ct_model>/<str:slug>/', OffersDetailView.as_view(), name='offers_detail'),