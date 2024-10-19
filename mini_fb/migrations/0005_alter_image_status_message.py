# Generated by Django 4.2.16 on 2024-10-17 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("mini_fb", "0004_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="status_message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="mini_fb.statusmessage",
            ),
        ),
    ]
