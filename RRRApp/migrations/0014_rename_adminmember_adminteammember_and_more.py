# Generated by Django 4.2.1 on 2023-11-03 22:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RRRApp', '0013_alter_merchitem_item_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdminMember',
            new_name='AdminTeamMember',
        ),
        migrations.RenameModel(
            old_name='TechincalMember',
            new_name='TechincalTeamMember',
        ),
    ]