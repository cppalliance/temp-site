# Generated by Django 4.2.16 on 2024-12-18 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("libraries", "0027_libraryversion_dependencies"),
        ("versions", "0015_drop_review_generated_stub_users"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="review_manager",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="managed_reviews",
                to="libraries.commitauthor",
            ),
        ),
        migrations.AlterField(
            model_name="review",
            name="submitters",
            field=models.ManyToManyField(
                related_name="submitted_reviews", to="libraries.commitauthor"
            ),
        ),
    ]
