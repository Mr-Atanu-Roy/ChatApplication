# Generated by Django 4.2.3 on 2023-08-12 10:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0014_remove_notification_message"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="friendrequests",
            name="message",
        ),
        migrations.AddField(
            model_name="notification",
            name="message",
            field=models.CharField(blank=True, max_length=655, null=True),
        ),
    ]
