# Generated by Django 5.1.1 on 2024-09-25 07:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("patients", "0007_alter_patient_phone_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="assessment",
        ),
        migrations.AddField(
            model_name="assessment",
            name="question",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name="Answer",
        ),
        migrations.DeleteModel(
            name="Question",
        ),
    ]
