# Generated by Django 4.2.3 on 2023-07-15 10:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("chat", "0004_alter_usercontacts_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercontacts",
            name="contacts",
            field=models.ManyToManyField(
                blank=True, null=True, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
