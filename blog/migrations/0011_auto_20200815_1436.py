# Generated by Django 3.0.8 on 2020-08-15 14:36

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200815_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogindexpage',
            name='categories',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='categories',
            field=modelcluster.fields.ParentalManyToManyField(blank=True, to='blog.BlogCategory'),
        ),
    ]
