# Generated by Django 5.0.1 on 2024-04-08 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('z', '0008_token_user_treasure_user_alter_photo_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='protected',
            field=models.BooleanField(db_default=models.Value(False)),
        ),
    ]
