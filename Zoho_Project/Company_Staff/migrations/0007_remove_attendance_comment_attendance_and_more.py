# Generated by Django 5.0 on 2024-02-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Staff', '0006_remove_attendance_comment_employee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance_comment',
            name='attendance',
        ),
        migrations.AddField(
            model_name='attendance_comment',
            name='month',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='attendance_comment',
            name='year',
            field=models.CharField(max_length=4, null=True),
        ),
    ]