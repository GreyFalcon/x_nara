from django.db import models


# Model Currency Pair
class CurrencyPair(models.Model):
    """
    This is the currency pair model.
    An entity is represented by the following attribute
    - currency_code: input currency code
    - language: the localization language
    - target_currency_code: the desired converted currency code
    """
    id = models.IntegerField(primary_key=True, auto_created=True)
    curr_code = models.CharField(max_length=64, name='curr_code', null=False)
    language = models.CharField(max_length=64, name='language', null=False)
    target_code = models.CharField(max_length=64, name='target_code', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('curr_code', 'language', 'target_code'),)

    def __str__(self):
        return f'{self.curr_code} is translated to {self.target_code} in {self.language}'
