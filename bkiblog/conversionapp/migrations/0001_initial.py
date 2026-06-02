# Generated migration

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHolding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gold18', models.DecimalField(decimal_places=3, default=0, help_text='Gold 18K in grams', max_digits=12)),
                ('gold24', models.DecimalField(decimal_places=3, default=0, help_text='Gold 24K in grams', max_digits=12)),
                ('usd', models.DecimalField(decimal_places=2, default=0, help_text='US Dollars', max_digits=12)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Holding',
                'verbose_name_plural': 'User Holdings',
            },
        ),
        migrations.CreateModel(
            name='NetWorthHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net_worth', models.DecimalField(decimal_places=2, help_text='Net worth in IRR', max_digits=18)),
                ('gold18_amount', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('gold24_amount', models.DecimalField(decimal_places=3, default=0, max_digits=12)),
                ('usd_amount', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='networth_history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Net Worth History',
                'verbose_name_plural': 'Net Worth Histories',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='networthhistory',
            index=models.Index(fields=['user', '-timestamp'], name='conversionapp_networthhistory_user_timestamp_idx'),
        ),
    ]
