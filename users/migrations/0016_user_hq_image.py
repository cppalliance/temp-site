# Generated by Django 4.2.16 on 2025-01-22 22:39

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0015_user_delete_permanently_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="hq_image",
            field=models.FileField(
                blank=True,
                help_text="A high-quality image of the user - used in profiles/reports.",
                null=True,
                upload_to="hiqh-quality-user-images",
                validators=[
                    core.validators.FileTypeValidator(
                        extensions=[".jpg", ".jpeg", ".png"]
                    ),
                    core.validators.MaxFileSizeValidator(max_size=52428800),
                ],
                verbose_name="High Quality Image",
            ),
        ),
    ]
