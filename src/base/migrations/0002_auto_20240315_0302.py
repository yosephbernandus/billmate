# Generated by Django 5.0.3 on 2024-03-15 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                (
                    """
                    ALTER table bill_group ADD name VARCHAR(255) NULL;
                    """
                ),
            ],
            reverse_sql=[
                (
                    """
                    ALTER table bill_group DROP COLUMN if exists name;
                    """
                )
            ]
        )
    ]