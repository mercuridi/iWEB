# Generated by Django 4.1.5 on 2023-03-22 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_alter_item_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='type',
            field=models.CharField(default='Fountain', max_length=50),
            preserve_default=False,
        ),
    ]