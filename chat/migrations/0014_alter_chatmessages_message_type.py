# Generated by Django 4.2.3 on 2023-07-29 18:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0013_chatmessages_file_chatmessages_message_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatmessages",
            name="message_type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("link", "Link"),
                    ("img", "Image"),
                    ("audio", "Audio"),
                    ("video", "Video"),
                    ("doc", "Document"),
                ],
                default="text",
                max_length=255,
            ),
        ),
    ]
