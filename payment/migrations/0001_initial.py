# Generated by Django 4.2 on 2023-04-03 15:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_code', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('paid_date', models.DateField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, null=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='payment.currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
