import qrcode.image.base
import qrcode.image.pil
from PIL import ImageDraw, Image
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from random import choice
from phonenumber_field.modelfields import PhoneNumberField


class Money(models.Model):
    """ Балансы пользователей
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sum = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Сумма')
    under_consideration = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='На рассмотрении')
    self_under_consideration = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        verbose_name='Личный зароботок. На рассмотрении'
    )
    available = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Средства на балансе')
    self_available = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0,
        verbose_name='Личный зароботок. Средства на балансе'
    )
    reserved = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Зарезервировано к выплате')
    accrued = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Начислено')
    paid_out = models.DecimalField(max_digits=7, decimal_places=2, default=0, verbose_name='Выплачено')

    class Meta:
        ordering = ('user', 'available',)
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'

    def __str__(self):
        return self.user.username


class ApplicationsForMoney(models.Model):
    """ Заявки на вывод денежных средств
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserved = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Зарезервированная сумма')
    card = models.CharField(max_length=16, verbose_name='На карту')
    is_processed = models.BooleanField(default=False, verbose_name='Обработано?')
    is_paid_out = models.BooleanField(default=False, verbose_name='Выплачено?')
    created_at = models.DateTimeField(verbose_name='Дата и время заявки', auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'Заявка на выплату'
        verbose_name_plural = 'Заявки на выплату'

    def __str__(self):
        return self.user.username


class ReferralCodes(models.Model):
    """ Уникальные реферальные коды пользователей
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=7, verbose_name='Реферальный код', unique=True)
    qr_code = models.ImageField(upload_to='qr_code', blank=True)

    class Meta:
        ordering = ('user', 'code',)
        verbose_name = 'Реферальный код'
        verbose_name_plural = 'Реферальная система'

    def __str__(self):
        return self.code


class Cards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.CharField(max_length=16, unique=True)

    class Meta:
        verbose_name = 'Карта для вывода средств'
        verbose_name_plural = 'Карты для вывода средств'

    def __str__(self):
        return self.card


class Profile(models.Model):
    """ Участники программы. Расширенная модель User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(null=True, blank=True)
    referred = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Ссылка наставника',
        related_name='referred',
        blank=True, null=True
    )
    referrer = models.CharField(max_length=30, verbose_name='Реферальная ссылка')
    location = models.CharField(max_length=30, verbose_name='Местоположение', blank=True, null=True)
    balance = models.ForeignKey(Money, on_delete=models.CASCADE, verbose_name='Баланс', related_name='balance')
    status = models.IntegerField(default=0, verbose_name='Статус')
    # messages = models.ManyToManyField('History', verbose_name='Соощщения', blank=True, null=True)
    struct1 = models.ManyToManyField(User, verbose_name='Уровень 1', related_name='struct_1', blank=True)
    struct2 = models.ManyToManyField(User, verbose_name='Уровень 2', related_name='struct_2', blank=True)
    struct3 = models.ManyToManyField(User, verbose_name='Уровень 3', related_name='struct_3', blank=True)
    struct4 = models.ManyToManyField(User, verbose_name='Уровень 4', related_name='struct_4', blank=True)
    struct5 = models.ManyToManyField(User, verbose_name='Уровень 5', related_name='struct_5', blank=True)
    struct = models.IntegerField(default=1, verbose_name='Структура')
    broker = models.BooleanField(default=False, verbose_name='Статус брокера')
    active_referrals = models.ManyToManyField(
        User,
        related_name='referrals_counts',
        verbose_name='Активные рефералы',
        blank=True,
    )
    broker_status = models.BooleanField(default=False, verbose_name='Вывод средств с личных продаж')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники программы'

    def __str__(self):
        return self.user.get_full_name()

    def sum(self):
        """ Сумма баланса """
        return self.balance.available + self.balance.self_available + self.balance.under_consideration + self.balance.self_available

    def available(self):
        """ Доступно для вывода """
        if self.broker_status:
            return self.balance.available + self.balance.self_available
        else:
            return self.balance.available

    def set_status(self, next_status=0):
        """ Установка статуса участника программы
            Если назначаемый статус равен 0 и текущий статус равен 0, то текущий статус увеличивается на 1
            Функция с такими условиями вызывается при оформлении оффера и выполнения целевых действий и дает право
            на получение реферальной ссылки
            :param next_status: - назначаемый статус
        """
        if not self.status and not next_status:
            self.status += 1
        elif next_status:
            self.status = next_status


class Orders(models.Model):
    """ Файлы отчетов с партнерской программы для распределения балансов между участниками по уровням
        И отчетов о зачислении зарезервированых для выплаты средств
        Удаляются автоматически
    """
    order = models.FileField(upload_to='uploads')


class History(models.Model):
    """ Сообщения истории действий пользователей (выплаты, переходы и тд...)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    action = models.TextField(verbose_name='Действие', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='Дата и время заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Системные сообщения'
        verbose_name_plural = 'Системные сообщения'


class FeedBackRequests(models.Model):
    """ Заявки обратной связи
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    theme = models.CharField(max_length=100, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(verbose_name='Дата и время сообщения', auto_now_add=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Сообщения обратной связи'

    def __str__(self):
        return self.theme


def get_unique_referral_url():
    """ Генерация уникального кода для реферальной ссылки
    :return: code - сгенерированный уникальный код
    """
    chars = [
        'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k',
        'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
        'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        '0', ]
    code = ''
    for _ in range(5):
        char = choice(chars)
        code += char
    return code


class PilImage(qrcode.image.pil.PilImage):
    def __init__(self, border, width, box_size):
        if Image is None and ImageDraw is None:
            raise NotImplementedError("PIL not available")
        qrcode.image.base.BaseImage.__init__(self, border, width, box_size)
        self.kind = "PNG"

        pixelsize = (self.width + self.border * 2) * self.box_size
        self._img = Image.new("RGBA", (pixelsize, pixelsize))
        self._idr = ImageDraw.Draw(self._img)


def make_qr_code(string):
    return qrcode.make(string, box_size=10, border=1, image_factory=PilImage)


@receiver(pre_delete, sender=Orders)
def delete_Orders_order(sender, instance, **kwargs):
    """ При удалении отчета (файла) удаляется сам файл.
        Удаление происходит сразу после загрузки и обработки отчета
    """
    if instance.order.name:
        instance.order.delete(False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ При создании нового пользователя создается его профиль
    """
    if created:
        code = ReferralCodes.objects.create(user=instance, code=get_unique_referral_url())
        balance = Money.objects.create(
            user=instance,
            under_consideration=0,
            available=0,
            reserved=0,
            accrued=0,
            paid_out=0
        )
        # balance = Money.objects.get(user=instance)
        Profile.objects.create(user=instance, balance=balance, referrer=f'http://myvmeste.info?r={code.code}')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    """ При создании нового пользователя создается его профиль
        СОХРАНЕНИЕ Профиля
    """
    instance.profile.save()

# @receiver(post_save, sender=History)
# def create_user_profile(sender, instance, created, **kwargs):
#     """ При создании новой карты она привязывается к пользователю
#     """
#     if created:
#         profile = Profile.objects.get(user=instance.user)
#         profile.messages.add(instance)
#         profile.save()
