# Generated by Django 5.0.6 on 2024-06-01 07:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='assigned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.member'),
        ),
        migrations.AddField(
            model_name='subtask',
            name='member_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.membertype'),
        ),
        migrations.AddField(
            model_name='task',
            name='assigned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='project.member'),
        ),
        migrations.AddField(
            model_name='task',
            name='member_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='project.membertype'),
        ),
    ]