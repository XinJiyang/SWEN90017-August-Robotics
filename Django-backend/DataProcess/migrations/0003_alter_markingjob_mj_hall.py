# Generated by Django 4.2.1 on 2023-09-15 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DataProcess', '0002_alter_employee_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='markingjob',
            name='mj_hall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marking_jobs', to='DataProcess.hall'),
        ),
    ]
