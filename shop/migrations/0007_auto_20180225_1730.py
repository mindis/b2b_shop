# Generated by Django 2.0.2 on 2018-02-25 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_shopconstant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='nophoto.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='productvariant',
            name='image',
            field=models.ImageField(default='nophoto.png', upload_to=''),
        ),
    ]
