# Generated by Django 4.1.3 on 2022-12-05 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sims_app', '0002_student_address_alter_student_other_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pay_date',
            field=models.DateField(null=True),
        ),
    ]
