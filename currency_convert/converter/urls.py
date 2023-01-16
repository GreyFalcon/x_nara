from django.urls import path

from converter.views import CurrencyPairViewSet

currency_pair_list = CurrencyPairViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

currency_pair_detail = CurrencyPairViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy',
})

currency_pair_convert = CurrencyPairViewSet.as_view({
    'get': 'convert',
})

urlpatterns = [
    path('', currency_pair_list, name='currency-pair-list'),
    path('<int:pk>', currency_pair_detail, name='currency-pair-detail'),
    path('<int:pk>/convert/<str:amount>', currency_pair_convert, name='currency-pair-convert'),
]