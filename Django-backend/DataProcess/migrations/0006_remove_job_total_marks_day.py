# Generated by Django 4.2.1 on 2023-10-27 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DataProcess', '0005_remove_markingjob_show_job_show_job_total_marks_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='total_marks_day',
        ),
    ]
