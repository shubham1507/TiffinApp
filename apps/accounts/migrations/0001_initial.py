# Generated by Django 3.0.2 on 2020-01-29 08:41

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('tiffin_provider_name', models.CharField(blank=True, max_length=300, verbose_name='Tifin Name')),
                ('is_seller', models.BooleanField(default=False, verbose_name='is seller')),
                ('is_buyer', models.BooleanField(default=False, verbose_name='is buyer')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone Number')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Date')),
                ('is_notification_sound', models.BooleanField(default=True)),
                ('is_notification_vibrate', models.BooleanField(default=True)),
                ('address_line_1', models.TextField(blank=True, null=True)),
                ('address_line_2', models.TextField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_seller_approved', models.BooleanField(default=False)),
                ('is_social', models.BooleanField(default=False)),
                ('food_type', models.CharField(choices=[('V', 'Veg'), ('N', 'Non-veg')], max_length=1)),
                ('pay', models.CharField(choices=[('M', 'Monthly'), ('W', 'Weekly'), ('O', 'Ontime')], max_length=1)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('validated_at', models.DateTimeField(blank=True, null=True)),
                ('validation_key', models.UUIDField(blank=True, default=uuid.uuid4, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
