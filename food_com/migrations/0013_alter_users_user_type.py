# Generated by Django 4.2.18 on 2025-02-27 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food_com', '0012_alter_users_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'Admin'), (2, 'Users')], default=2),
        ),
    ]
