# Generated by Django 4.2.3 on 2023-07-29 09:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0011_alter_group_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="group",
            options={
                "ordering": ["-created_at"],
                "verbose_name_plural": "Conversat Groups",
            },
        ),
    ]
