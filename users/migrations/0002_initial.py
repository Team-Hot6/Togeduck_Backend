# Generated by Django 4.1.2 on 2022-12-02 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('workshops', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hobby',
            field=models.ManyToManyField(to='workshops.hobby'),
        ),
    ]