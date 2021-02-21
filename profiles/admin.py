from django.contrib import admin
from .models import Profile, ReferralCodes, Money, ApplicationsForMoney, Cards, FeedBackRequests, History



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('first_name', 'last_name', 'under_consideration', 'available', 'reserved', 'paid_out',
                       'referred_first_name', 'referred_last_name', 'referred_location',)
    list_display = ['id', 'first_name', 'last_name', 'user']
    list_filter = ['location']
    fieldsets = (
        ('Данные', {
            'fields': ('first_name', 'last_name', 'phone', 'location', 'referrer', 'user', 'status'),
        }),
        ('Баланс', {
            'fields': ('under_consideration', 'available', 'reserved', 'paid_out',),
        }),
        ('Наставник', {
            'fields': ('referred_last_name', 'referred_first_name', 'referred_location', 'referred',),
        }),
    )

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def under_consideration(self, obj):
        return obj.balance.under_consideration

    def available(self, obj):
        return obj.balance.available

    def reserved(self, obj):
        return obj.balance.reserved

    def paid_out(self, obj):
        return obj.balance.paid_out

    def referred_first_name(self, obj):
        if obj.referred.first_name:
            return obj.referred.first_name
        else:
            return 'Отсутствует'

    def referred_last_name(self, obj):
        if obj.referred.last_name:
            return obj.referred.last_name
        else:
            return 'Отсутствует'

    def referred_location(self, obj):
        if obj.referred.profile.location:
            return obj.referred.pofile.location
        else:
            return 'Отсутствует'

    first_name.short_description = 'Имя'
    last_name.short_description = 'Фмилия'
    under_consideration.short_description = 'На рассмотрении'
    available.short_description = 'Средства на балансе'
    reserved.short_description = 'Зарезервировано к выплате'
    paid_out.short_description = 'Выплачено'
    referred_first_name.short_description = 'Имя наставника'
    referred_last_name.short_description = 'Фамилия наставника'
    referred_location.short_description = 'Город наставника'



@admin.register(ReferralCodes)
class ReferralCodesAdmin(admin.ModelAdmin):
    list_display = ['user', 'code']



@admin.register(Money)
class MoneyAdmin(admin.ModelAdmin):
    list_display = ['user', 'available', 'under_consideration']



@admin.register(ApplicationsForMoney)
class ApplicationsForMoneyAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'reserved', 'is_processed', 'is_paid_out', 'created_at']
    list_filter = ['is_processed', 'is_paid_out']


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):
    list_display = ['user', 'card']


@admin.register(FeedBackRequests)
class FeedBackRequestsAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'created_at']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'action', 'created_at']