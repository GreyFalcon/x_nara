import requests
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action

from converter.models import CurrencyPair
from converter.serializer import CurrencyPairSerializer


class CurrencyPairViewSet(viewsets.ModelViewSet):
    """
    The ModelViewSet definition for the CurrencyPair model
    The default CRUD operation support is built-in in the ModelViewSet
    """
    serializer_class = CurrencyPairSerializer
    queryset = CurrencyPair.objects.all()

    EXCHANGE_API = 'https://xnara-hiring-default-rtdb.asia-southeast1.firebasedatabase.app/currencyrate.json'
    CURRENCY_API = 'https://xnara-hiring-default-rtdb.asia-southeast1.firebasedatabase.app/currencyprops.json'

    @action(detail=True)
    def convert(self, request, *args, **kwargs):
        # check if there is a valid currency pair in configuration
        convert_conf: CurrencyPair = get_object_or_404(self.queryset, pk=kwargs['pk'])

        # get the input value
        input_value = float(kwargs['amount'])

        # Get the exchange configuration from the firebase DB
        # TODO: Fetch once and store in cache at start - refresh after periodic interval perhaps
        exchange_conf_response = requests.get(CurrencyPairViewSet.EXCHANGE_API)
        if exchange_conf_response.status_code != 200:
            raise BadRequest('Failed to fetch exchange configuration')
        exchange_conf = exchange_conf_response.json()

        conf_dict: dict = {}
        base_currency: str = None

        # Generate the exchange configuration as a dict for easy lookup
        for conf in exchange_conf:
            conf_dict[conf['currency_code']] = conf['rate_modifier']
            if conf['is_base']:
                base_currency = conf['currency_code']

        if convert_conf.curr_code != base_currency:
            input_value = input_value / conf_dict[convert_conf.curr_code]
        converted_currency = input_value * conf_dict[convert_conf.target_code]

        currency_properties_resp = requests.get(CurrencyPairViewSet.CURRENCY_API)
        if currency_properties_resp.status_code != 200:
            raise BadRequest('Failed to fetch currency format configuration')
        currency_properties = currency_properties_resp.json()
        # Generate the exchange configuration as a dict for easy lookup
        for conf in currency_properties:
            conf_dict[conf['currency_code']] = (conf['decimal_places'], conf['symbol'])
        decimal_place, symbol = conf_dict[convert_conf.target_code]
        converted_currency_str: str = f'{symbol} {(round(converted_currency, decimal_place))}'

        # TODO: internationalization to be added
        response_payload = {
            'result': converted_currency,
            'statement': converted_currency_str,
        }
        return JsonResponse(response_payload)

