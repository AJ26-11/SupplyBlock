# Generated by Django 4.0.5 on 2023-10-27 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyChainData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('blockchain_tx_id', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
