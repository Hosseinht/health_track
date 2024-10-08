# Generated by Django 5.1.1 on 2024-09-24 07:39

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0002_rename_patients_patient"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="clinician",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Assessment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "assessment_type",
                    models.CharField(
                        choices=[
                            ("cognitive", "Cognitive Status"),
                            ("physical", "Physical Ability"),
                            ("mental", "Mental Health"),
                            ("emotional", "Emotional Well-being"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "assessment_data",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2024, 9, 24, 7, 39, 37, 19765, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
                ("final_score", models.SmallIntegerField()),
                (
                    "clinician",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patients.patient",
                    ),
                ),
            ],
        ),
    ]
