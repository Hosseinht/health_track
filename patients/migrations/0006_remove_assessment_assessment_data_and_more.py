# Generated by Django 5.1.1 on 2024-09-25 05:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0005_alter_address_address_two_alter_answer_question_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="assessment",
            name="assessment_data",
        ),
        migrations.AddField(
            model_name="assessment",
            name="assessment_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="patient",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="patient",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
