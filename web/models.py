from django.db import models
from django.urls import reverse


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_model_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname=viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_categories_count(self):
        models = get_models_for_count('debet_kards', 'credit_kards')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url())
            for c in qs
        ]
        return data


class Categories(models.Model):
    """ Категории
    """
    name = models.CharField(max_length=250, verbose_name='Имя')
    slug = models.CharField(max_length=250, verbose_name='Ссылка')
    image = models.ImageField(upload_to='images/categories', verbose_name='Изображение', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    objects = CategoryManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = '- Категории -'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Offers(models.Model):
    """ Офферы (Родительский класс)
    """
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Категория')
    offer_id = models.CharField(max_length=50, verbose_name='ID оффера', blank=True, null=True)
    bank_name = models.CharField(max_length=250, verbose_name='Банк')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    slug = models.CharField(max_length=250, verbose_name='Ссылка')
    reward = models.PositiveIntegerField(verbose_name='Вознаграждение')
    main_characteristics = models.TextField(verbose_name='Основные характеристики', blank=True, null=True)
    condition = models.TextField(db_index=True, verbose_name='Описание условия')
    short_condition = models.CharField(max_length=250, db_index=True, verbose_name='Краткое описание условия')
    demands = models.CharField(max_length=250, verbose_name='Требования', blank=True, null=True)
    recommend = models.BooleanField(verbose_name='Рекомендуем')
    max_pay = models.BooleanField(verbose_name='Макс выплата')
    popular = models.BooleanField(verbose_name='Популярный')
    referral_slug = models.CharField(
        max_length=250,
        db_index=True,
        verbose_name='Реферальная ссылка на продукт 1',
        null=True,
        blank=True
    )
    referral_slug_2 = models.CharField(
        max_length=250,
        db_index=True,
        verbose_name='Реферальная ссылка на продукт 2',
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('offers_detail', kwargs={'ct_model': self.category.slug, 'slug': self.slug})


class CreditCards(Offers):
    """ Кредитные карты
    """
    card_name = models.CharField(max_length=250, db_index=True, verbose_name='Название карты')
    limit = models.PositiveIntegerField(verbose_name='Кредитный лимит')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    installment_plan = models.PositiveIntegerField(verbose_name='Рассрочка', null=True, blank=True)
    grace_period = models.PositiveIntegerField(verbose_name='Льготный период', null=True, blank=True)
    delivery = models.BooleanField(verbose_name='Доставка')

    class Meta:
        ordering = ('bank_name', 'card_name',)
        verbose_name = 'Кредитная карта'
        verbose_name_plural = 'Кредитные карты'

    def __str__(self):
        return self.card_name


class DebitCards(Offers):
    """ Дебитовые карты
    """
    card_name = models.CharField(max_length=250, db_index=True, verbose_name='Название карты')
    service_cost = models.PositiveIntegerField(verbose_name='Стоимость обслуживания')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    cash_back = models.FloatField(verbose_name='Кэшбэк', null=True, blank=True)
    miles = models.PositiveIntegerField(verbose_name='Мили', null=True, blank=True)
    delivery = models.BooleanField(verbose_name='Доставка')

    class Meta:
        ordering = ('bank_name', 'card_name',)
        verbose_name = 'Дебетовая карта'
        verbose_name_plural = 'Дебетовые карты'

    def __str__(self):
        return self.card_name


class Credits(Offers):
    """ Родительский класс для моделей кредитов
        Потреб, Ипотека, Рефенансирование
    """
    type = models.CharField(max_length=250, db_index=True, verbose_name='Тип кредита')
    limit = models.PositiveIntegerField(verbose_name='Кредитный лимит')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    documents = models.CharField(max_length=250, verbose_name='Требуемые документы')
    percents = models.FloatField(verbose_name='Процентная ставка')

    class Meta:
        ordering = ('bank_name', 'type',)
        verbose_name = 'Кредит'
        verbose_name_plural = 'Кредиты'

    def __str__(self):
        return self.bank_name


class MFO(Offers):
    """ МФО
    """
    term = models.PositiveIntegerField(verbose_name='Срок займа')
    age = models.PositiveIntegerField(verbose_name='Возраст')
    sum = models.PositiveIntegerField(verbose_name='Сумма займа')
    percents = models.FloatField(verbose_name='Ставка займа')

    class Meta:
        ordering = ('bank_name',)
        verbose_name = 'Микрозайм'
        verbose_name_plural = 'Микрозаймы'

    def __str__(self):
        return self.bank_name


class PotrebCredits(Credits):
    """ Потребительские кредиты
    """
    class Meta:
        ordering = ('bank_name', 'type',)
        verbose_name = 'Потребительский кредит'
        verbose_name_plural = 'Потребительские кредиты'

    def __str__(self):
        return self.bank_name


class Mortgages(Credits):
    """ Ипотечные кредиты
    """
    class Meta:
        ordering = ('bank_name', 'type',)
        verbose_name = 'Ипотечный кредит'
        verbose_name_plural = 'Ипотечные кредиты'

    def __str__(self):
        return self.bank_name


class RKO(Offers):
    """ Рассчетно кассовое оборудование
    """
    payments = models.CharField(max_length=250, db_index=True, verbose_name='Платежи')
    cash_deposit = models.FloatField(verbose_name='Внесение наличных')
    service_cost = models.FloatField(verbose_name='Стоимость обслуживания')
    cash_withdrawal = models.FloatField(verbose_name='Снятие наличных')

    class Meta:
        ordering = ('bank_name',)
        verbose_name = 'Рассчетно кассовое обслуживание'
        verbose_name_plural = 'Рассчетно кассовое обслуживание '

    def __str__(self):
        return self.bank_name


class Refinancing(Credits):
    """ Рефенансирование
    """
    class Meta:
        ordering = ('bank_name', 'type',)
        verbose_name = 'Рифенансирование'
        verbose_name_plural = 'Рефинансирование'

    def __str__(self):
        return self.bank_name


class IDOrders(models.Model):
    """ Отчеты с партнерской программы
    """
    order_id = models.CharField(max_length=250, verbose_name='ID Отчета', unique=True)
    offer_id = models.PositiveIntegerField(verbose_name='ID Оффера')
    status = models.CharField(max_length=250, db_index=True, verbose_name='Статус')

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = '-Отчеты-'

