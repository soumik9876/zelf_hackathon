# Generated by Django 4.1.6 on 2024-02-03 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authorinfo',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='authorinfo',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='authorstats',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='authorstats',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='contentstats',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='contentstats',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='context',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='context',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='media',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='media',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='origindetails',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='origindetails',
            name='modified_date',
        ),
    ]
