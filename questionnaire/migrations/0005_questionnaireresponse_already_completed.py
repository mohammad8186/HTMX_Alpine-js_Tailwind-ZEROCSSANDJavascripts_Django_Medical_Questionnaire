# Generated by Django 5.1.3 on 2025-02-25 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_alter_questionnaireresponse_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaireresponse',
            name='already_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
