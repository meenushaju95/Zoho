# Generated by Django 5.0 on 2024-02-10 05:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company_Staff', '0009_alter_attendance_comment_month_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_comment',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Company_Staff.payroll_employee'),
        ),
    ]
