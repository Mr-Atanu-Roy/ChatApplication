# Generated by Django 4.2.3 on 2023-07-29 18:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0014_alter_chatmessages_message_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatmessages",
            name="message",
            field=models.CharField(blank=True, max_length=650, null=True),
        ),
    ]
