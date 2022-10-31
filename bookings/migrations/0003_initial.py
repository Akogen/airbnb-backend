# Generated by Django 4.1.2 on 2022-10-31 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("bookings", "0002_initial"),
        ("rooms", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bookings",
                to="rooms.room",
            ),
        ),
    ]
