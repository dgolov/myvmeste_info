from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import NON_FIELD_ERRORS, MultipleObjectsReturned
from django import forms
from .models import Orders, ApplicationsForMoney, Cards, Profile, FeedBackRequests


class UserRegistrationForm(UserCreationForm):
    """ Форма регистрации пользователя
    """
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин...', 'style': 'width: 96%;'}))
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email...', 'style': 'width: 96%;'}))
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя...', 'style': 'width: 96%;'}))
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия...', 'style': 'width: 96%;'}))
    location = forms.CharField(
        label='Город',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город...', 'style': 'width: 96%;'}))
    phone = PhoneNumberField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона...',
                                      'style': 'width: 96%;'}),
        error_messages={NON_FIELD_ERRORS: {'Введите номе телефона',}})
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль...', 'style': 'width: 96%;'}))
    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повтор пароля...',
                                          'style': 'width: 96%;'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        cd = self.cleaned_data
        try:
            User.objects.get(email=cd['email'])
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        except User.DoesNotExist:
            return cd['email']

    def clean_phone(self):
        cd = self.cleaned_data
        try:
            Profile.objects.get(phone=cd['phone'])
            raise forms.ValidationError('Пользователь с таким номером уже существует.')
        except Profile.DoesNotExist:
            return cd['phone']

    def clean_username(self):
        cd = self.cleaned_data
        if len(cd['username']) < 5:
            raise forms.ValidationError('Логин должен содержать не менее 5 символов.')
        return cd['username']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        elif len(password2) < 8:
            raise forms.ValidationError('Пароль должен содержать не менее 8 символов.')
        return password2


class UserSettingsForm(forms.ModelForm):
    """ Форма настроек пользователя
    """
    first_name = forms.CharField(
        label='Имя',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 96%;'})
    )
    last_name = forms.CharField(
        label='Фамилия',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 96%;'})
    )
    location = forms.CharField(
        label='Город', max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 96%;'})
    )
    email = forms.EmailField(
        label='E-mail', max_length=100,
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 96%;'}),
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        cd = self.cleaned_data
        if len(cd) > 2:
            try:
                User.objects.get(email=cd['email'])
                raise forms.ValidationError('Пользователь с таким email уже существует.')
            except User.DoesNotExist:
                return cd['email']
            except User.MultipleObjectsReturned:
                pass


class ChangePhoneForm(forms.Form):
    phone = PhoneNumberField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона...',
                                      'style': 'width: 100%;'})
    )

    class Meta:
        model: Profile
        fields = ('phone',)

    def clean_phone(self):
        cd = self.cleaned_data
        try:
            Profile.objects.get(phone=cd['phone'])
            raise forms.ValidationError('Пользователь с таким номером уже существует.')
        except Profile.DoesNotExist:
            return cd['phone']


class UploadFileForm(forms.Form):
    """ Форма загрузки отчета от партнерской программы
    """
    report = forms.FileField()

    class Meta:
        model = Orders
        fields = ('order', )


class UploadOrderPayForm(forms.Form):
    """ Форма загрузки отчета выплат денежных средств
    """
    report_pay = forms.FileField()

    class Meta:
        model = Orders
        fields = ('order', )


class ApplicationsForMoneyForm(forms.Form):
    """ Форма заявки на вывод денежных средств
    """
    reserved = forms.DecimalField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
        validators=[MinValueValidator(1000)]
    )

    class Meta:
        model = ApplicationsForMoney
        fields = ('reserved', )


class AddCardsForm(forms.ModelForm):
    """ Форма добавления карты
    """
    card = forms.CharField(
        label='Номер карты',
        max_length=16,
        min_length=16,
        widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'number', 'style': 'width: 100%;'})
    )

    class Meta:
        model = Cards
        fields = ('card', )


class FeedBackForm(forms.ModelForm):
    """ Форма обратной связи
    """
    class Meta:
        model = FeedBackRequests
        fields = ('theme', 'message',)
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 100%;'}),
            'message': forms.Textarea(attrs={'class': 'form-controls', 'style': 'width: 100%; height: 250px;'})
        }