# Generated by Django 5.2.3 on 2025-06-18 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_issue_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
