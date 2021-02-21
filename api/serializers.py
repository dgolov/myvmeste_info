from django.contrib.auth.models import User
from rest_framework import serializers
from web.models import Categories, CreditCards, DebitCards, RKO, Mortgages, PotrebCredits, MFO, Refinancing


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """ Сералайзер модели пользователя
    """
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class CategorySerializer(serializers.ModelSerializer):
    """ Сералайзер модели категорий
    """
    class Meta:
        model = Categories
        fields = ['id', 'name', 'slug', 'image', 'is_active']


class BaseOfferSerializer:
    """ Базовый сералайзер офферов
    """
    category = serializers.PrimaryKeyRelatedField(queryset=Categories.objects)
    offer_id = serializers.CharField(required=False)
    bank_name = serializers.CharField(required=True)
    image = serializers.ImageField(required=True)
    slug = serializers.CharField(required=True)
    reward = serializers.IntegerField(required=True)
    main_characteristics = serializers.CharField(required=False)
    condition = serializers.CharField(required=True)
    short_condition = serializers.CharField(required=True)
    demands = serializers.CharField(required=False)
    recommend = serializers.BooleanField(required=True)
    max_pay = serializers.BooleanField(required=True)
    popular = serializers.BooleanField(required=True)
    referral_slug = serializers.CharField(required=False)
    is_active = serializers.BooleanField(default=True)


class BaseCreditSerializer(BaseOfferSerializer):
    """ Базовый сералайзер кредитов
    """
    type = serializers.CharField(required=True)
    limit = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=True)
    documents = serializers.CharField(required=True)
    percents = serializers.FloatField(required=True)


class CreditCardsSerializer(BaseOfferSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Кредитные карты
    """
    card_name = serializers.CharField(required=True)
    limit = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=True)
    installment_plan = serializers.IntegerField(required=False)
    grace_period = serializers.IntegerField(required=False)
    delivery = serializers.BooleanField(required=False)

    class Meta:
        model = CreditCards
        fields = '__all__'


class DebitCardsSerializer(BaseOfferSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Дебетовые карты
    """
    card_name = serializers.CharField(required=True)
    service_cost = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=True)
    cash_back = serializers.FloatField(required=False)
    miles = serializers.IntegerField(required=False)
    delivery = serializers.BooleanField(required=False)

    class Meta:
        model = DebitCards
        fields = '__all__'


class PotrebCreditsSerializer(BaseCreditSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Потребительские кредиты
    """
    class Meta:
        model = PotrebCredits
        fields = '__all__'


class MortgagesSerializer(BaseCreditSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Ипотера
    """
    class Meta:
        model = Mortgages
        fields = '__all__'


class RefinancingSerializer(BaseCreditSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Рефенансирование
    """
    class Meta:
        model = Refinancing
        fields = '__all__'


class MFOSerializer(BaseOfferSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Дебетовые карты
    """
    term = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=True)
    sum = serializers.IntegerField(required=True)
    percents = serializers.FloatField(required=True)

    class Meta:
        model = MFO
        fields = '__all__'


class RKOSerializer(BaseOfferSerializer, serializers.ModelSerializer):
    """ Сералайзер модели Дебетовые карты
    """
    payments = serializers.CharField(required=True)
    cash_deposit = serializers.FloatField(required=True)
    service_cost = serializers.FloatField(required=True)
    cash_withdrawal = serializers.FloatField(required=True)

    class Meta:
        model = RKO
        fields = '__all__'
