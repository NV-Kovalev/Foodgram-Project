# Generated by Django 4.2.2 on 2023-06-26 16:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_email_alter_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(error_messages={'max_length': 'Поле должно быть короче 150 символов'}, max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z', 'Неправильное значение username Это поле может содержать только буквы, цифры, а также символы ".@+-"')], verbose_name='Никнейм пользователя'),
        ),
    ]
