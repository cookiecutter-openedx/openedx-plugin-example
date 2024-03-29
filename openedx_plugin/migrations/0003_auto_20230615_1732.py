# coding=utf-8
# Generated by Django 3.2.19 on 2023-06-15 17:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("openedx_plugin", "0002_alter_marketingsites_language"),
    ]

    operations = [
        migrations.AlterField(
            model_name="configuration",
            name="type",
            field=models.CharField(
                choices=[("dev", "Development"), ("test", "Testing / QA"), ("prod", "Production")],
                default="dev",
                help_text="Type of Open edX environment in which this configuration                 will be used.",
                max_length=24,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="locale",
            name="url",
            field=models.URLField(
                help_text="URL for for anchor tag for this language.                 Example: https://example.org/contact/"
            ),
        ),
        migrations.AlterField(
            model_name="marketingsites",
            name="province",
            field=models.CharField(
                blank=True,
                help_text="A sub-region for the language code. Example: for language code            "
                " en-US valid possibles include TX, FL, CA, DC, KY, etc.",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="marketingsites",
            name="site_url",
            field=models.URLField(
                default="https://example.org",
                help_text="URL for for anchor tag for this language.                     Example: https://example.org/contact/",
            ),
        ),
    ]
