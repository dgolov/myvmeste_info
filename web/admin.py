from django.contrib import admin
from .models import Categories, DebitCards, CreditCards, PotrebCredits, MFO, Mortgages, RKO, Refinancing, IDOrders
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


admin.site.site_header = '"Мы Вместе" панель управления'
admin.site.site_title = 'МыВместе'


class AdminDebitCardsForm(forms.ModelForm):
    condition = forms.CharField(label='Описание', widget=CKEditorUploadingWidget)

    class Meta:
        model: DebitCards
        fields = '__all__'


class AdminCreditCardsForm(forms.ModelForm):
    condition = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model: CreditCards
        fields = '__all__'


class AdminPotrebCreditsForm(forms.ModelForm):
    condition = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model: PotrebCredits
        fields = '__all__'


class AdminMortgagesForm(forms.ModelForm):
    condition = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model: Mortgages
        fields = '__all__'


class AdminRefinancingForm(forms.ModelForm):
    condition = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model: Refinancing
        fields = '__all__'


class AdminMFOForm(forms.ModelForm):
    condition = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model: MFO
        fields = '__all__'


class AdminRKOForm(forms.ModelForm):
    condition = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model: RKO
        fields = '__all__'


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DebitCards)
class DebitCardsAdmin(admin.ModelAdmin):
    form = AdminDebitCardsForm
    list_display = ['bank_name', 'card_name', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('card_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'card_name', 'image', 'slug', 'main_characteristics',
                       'condition', 'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('service_cost', 'age', 'cash_back', 'miles', 'delivery', 'demands', 'recommend', 'max_pay',
                       'popular', 'is_active'),
        }),
    )


@admin.register(CreditCards)
class CreditCardsAdmin(admin.ModelAdmin):
    form = AdminCreditCardsForm
    list_display = ['bank_name', 'card_name', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('card_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'card_name', 'image', 'slug', 'condition',
                       'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('grace_period', 'installment_plan', 'age', 'limit', 'delivery', 'demands', 'recommend',
                       'max_pay', 'popular', 'is_active'),
        }),
    )


@admin.register(PotrebCredits)
class PotrebCreditsAdmin(admin.ModelAdmin):
    form = AdminPotrebCreditsForm
    list_display = ['bank_name', 'type', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active', 'type']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('bank_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'type', 'image', 'slug', 'main_characteristics',
                       'condition', 'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('age', 'limit', 'percents', 'documents', 'demands', 'recommend', 'max_pay', 'popular',
                       'is_active'),
        }),
    )


@admin.register(MFO)
class MFOAdmin(admin.ModelAdmin):
    form = AdminMFOForm
    list_display = ['bank_name', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('bank_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'image', 'slug', 'main_characteristics',
                       'condition', 'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('term', 'age', 'sum', 'percents', 'demands', 'recommend', 'max_pay', 'popular', 'is_active'),
        }),
    )


@admin.register(Mortgages)
class MortgagesAdmin(admin.ModelAdmin):
    form = AdminMortgagesForm
    list_display = ['bank_name', 'type', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('bank_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'type', 'image', 'slug', 'main_characteristics',
                       'condition', 'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('age', 'limit', 'percents', 'documents', 'demands', 'recommend', 'max_pay', 'popular',
                       'is_active'),
        }),
    )


@admin.register(RKO)
class RKOAdmin(admin.ModelAdmin):
    form = AdminRKOForm
    list_display = ['bank_name', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('bank_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'image', 'slug', 'main_characteristics',
                       'condition', 'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('payments', 'cash_deposit', 'service_cost', 'cash_withdrawal', 'demands', 'recommend', 'max_pay',
                       'popular', 'is_active'),
        }),
    )


@admin.register(Refinancing)
class RefinancingAdmin(admin.ModelAdmin):
    form = AdminRefinancingForm
    list_display = ['bank_name', 'type', 'reward', 'is_active']
    list_filter = ['bank_name', 'is_active']
    list_editable = ['reward', 'is_active']
    prepopulated_fields = {'slug': ('bank_name',)}
    fieldsets = (
        ('Общее', {
            'fields': ('category', 'offer_id', 'bank_name', 'type', 'image', 'slug', 'main_characteristics',
                       'condition', 'short_condition', 'referral_slug', 'referral_slug_2', 'reward'),
        }),
        ('Характеристики', {
            'fields': ('age', 'limit', 'percents', 'documents', 'demands', 'recommend', 'max_pay', 'popular',
                       'is_active'),
        }),
    )


@admin.register(IDOrders)
class IDOrdersAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_id', 'offer_id', 'status', 'broker']
    list_filter = ['status', 'offer_id']
