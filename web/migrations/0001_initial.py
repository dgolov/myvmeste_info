# Generated by Django 3.1.5 on 2021-01-30 15:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=250, verbose_name='Имя')),
                ('slug', models.CharField(db_index=True, max_length=250, verbose_name='Ссылка')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/categories', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': '- Категории -',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IDOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveIntegerField(unique=True, verbose_name='ID Отчета')),
                ('offer_id', models.PositiveIntegerField(verbose_name='ID Оффера')),
                ('status', models.CharField(db_index=True, max_length=250, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Отчет',
                'verbose_name_plural': '-Отчеты-',
            },
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='ID оффера')),
                ('bank_name', models.CharField(max_length=250, verbose_name='Банк')),
                ('image', models.ImageField(upload_to='images', verbose_name='Изображение')),
                ('slug', models.CharField(db_index=True, max_length=250, verbose_name='Ссылка')),
                ('reward', models.PositiveIntegerField(verbose_name='Вознаграждение')),
                ('main_characteristics', models.TextField(blank=True, null=True, verbose_name='Основные характеристики')),
                ('condition', models.TextField(db_index=True, verbose_name='Описание условия')),
                ('short_condition', models.CharField(db_index=True, max_length=250, verbose_name='Краткое описание условия')),
                ('recommend', models.BooleanField(verbose_name='Рекомендуем')),
                ('max_pay', models.BooleanField(verbose_name='Макс выплата')),
                ('popular', models.BooleanField(verbose_name='Популярный')),
                ('referral_slug', models.CharField(blank=True, db_index=True, max_length=250, null=True, verbose_name='Реферальная ссылка на продукт')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.categories', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='CreditCards',
            fields=[
                ('offers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.offers')),
                ('card_name', models.CharField(db_index=True, max_length=250, verbose_name='Название карты')),
                ('limit', models.PositiveIntegerField(verbose_name='Кредитный лимит')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('installment_plan', models.PositiveIntegerField(blank=True, null=True, verbose_name='Рассрочка')),
                ('grace_period', models.PositiveIntegerField(blank=True, null=True, verbose_name='Льготный период')),
                ('delivery', models.BooleanField(verbose_name='Доставка')),
            ],
            options={
                'verbose_name': 'Кредитная карта',
                'verbose_name_plural': 'Кредитные карты',
                'ordering': ('bank_name', 'card_name'),
            },
            bases=('web.offers',),
        ),
        migrations.CreateModel(
            name='Credits',
            fields=[
                ('offers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.offers')),
                ('type', models.CharField(db_index=True, max_length=250, verbose_name='Тип кредита')),
                ('limit', models.PositiveIntegerField(verbose_name='Кредитный лимит')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('documents', models.CharField(db_index=True, max_length=250, verbose_name='Требуемые документы')),
                ('percents', models.FloatField(verbose_name='Процентная ставка')),
            ],
            options={
                'verbose_name': 'Потребительский кредит',
                'verbose_name_plural': 'Потребительские кредиты',
                'ordering': ('bank_name', 'type'),
            },
            bases=('web.offers',),
        ),
        migrations.CreateModel(
            name='DebitCards',
            fields=[
                ('offers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.offers')),
                ('card_name', models.CharField(db_index=True, max_length=250, verbose_name='Название карты')),
                ('service_cost', models.PositiveIntegerField(verbose_name='Стоимость обслуживания')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('cash_back', models.FloatField(blank=True, null=True, verbose_name='Кэшбэк')),
                ('miles', models.PositiveIntegerField(blank=True, null=True, verbose_name='Мили')),
                ('delivery', models.BooleanField(verbose_name='Доставка')),
            ],
            options={
                'verbose_name': 'Дебетовая карта',
                'verbose_name_plural': 'Дебетовые карты',
                'ordering': ('bank_name', 'card_name'),
            },
            bases=('web.offers',),
        ),
        migrations.CreateModel(
            name='MFO',
            fields=[
                ('offers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.offers')),
                ('term', models.PositiveIntegerField(verbose_name='Срок займа')),
                ('age', models.PositiveIntegerField(verbose_name='Возраст')),
                ('decision', models.PositiveIntegerField(verbose_name='Решение по заявке')),
                ('percents', models.FloatField(verbose_name='Процентная ставка')),
            ],
            options={
                'verbose_name': 'Микрозайм',
                'verbose_name_plural': 'Микрозаймы',
                'ordering': ('bank_name',),
            },
            bases=('web.offers',),
        ),
        migrations.CreateModel(
            name='RKO',
            fields=[
                ('offers_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.offers')),
                ('payments', models.CharField(db_index=True, max_length=250, verbose_name='Платежи')),
                ('cash_deposit', models.FloatField(verbose_name='Внесение наличных')),
                ('service_cost', models.PositiveIntegerField(verbose_name='Стоимость обслуживания')),
                ('cash_withdrawal', models.PositiveIntegerField(verbose_name='Снятие наличных')),
            ],
            options={
                'verbose_name': 'Рассчетно кассовое оборудование',
                'verbose_name_plural': 'Рассчетно кассовое оборудование',
                'ordering': ('bank_name',),
            },
            bases=('web.offers',),
        ),
        migrations.CreateModel(
            name='Mortgages',
            fields=[
                ('credits_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.credits')),
            ],
            options={
                'verbose_name': 'Ипотечный кредит',
                'verbose_name_plural': 'Ипотечные кредиты',
                'ordering': ('bank_name', 'type'),
            },
            bases=('web.credits',),
        ),
        migrations.CreateModel(
            name='Refinancing',
            fields=[
                ('credits_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='web.credits')),
            ],
            options={
                'verbose_name': 'Рефенансирование',
                'verbose_name_plural': 'Рефенансирование',
                'ordering': ('bank_name', 'type'),
            },
            bases=('web.credits',),
        ),
    ]
