# Generated by Django 4.0.5 on 2022-06-09 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('softdesk_api', '0003_alter_issue_assignee_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributor',
            name='permission',
            field=models.CharField(choices=[('Contributor', 'CONTRIBUTOR'), ('Author', 'AUTHOR')], max_length=15),
        ),
    ]
