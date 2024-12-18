# Generated by Django 4.2.16 on 2024-12-10 22:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("film_log", "0004_remove_review_userprofile_review_user_profile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review", old_name="user_profile", new_name="userProfile",
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="movie",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlist",
                to="film_log.movie",
            ),
        ),
    ]
