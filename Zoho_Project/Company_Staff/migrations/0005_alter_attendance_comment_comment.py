# Generated by Django 5.0 on 2024-02-09 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Staff', '0004_attendance_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_comment',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]
