# Generated by Django 5.0.6 on 2024-06-02 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_remove_subtaskcomment_member_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtaskcomment',
            name='submited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='taskcomment',
            name='submited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]