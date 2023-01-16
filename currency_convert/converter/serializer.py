from rest_framework import serializers

from converter.models import CurrencyPair


class CurrencyPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyPair
        fields = ['id', 'curr_code', 'language', 'target_code']
