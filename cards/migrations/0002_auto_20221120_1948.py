# Generated by Django 3.2.13 on 2022-11-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercomment',
            name='is_opened',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='groupcard',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='groupcard',
            name='is_private',
            field=models.BooleanField(blank=True),
        ),
        migrations.AlterField(
            model_name='groupcard',
            name='title',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='content',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='usercomment',
            name='socks',
            field=models.IntegerField(blank=True),
        ),
    ]
