# 관리자계정 by gemini

from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

    if not User.objects.filter(username=ADMIN_USERNAME).exists():
        print(f'Creating superuser: {ADMIN_USERNAME}')
        User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD
        )
    else:
        print(f'Superuser {ADMIN_USERNAME} already exists.')


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0006_alter_answersubmission_options_alter_erratum_options_and_more'),
    ]

    operations = [
        # migrations.RunPython(create_superuser),
    ]