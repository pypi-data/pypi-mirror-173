from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('consents', '0001_initial'),
        ('subjects', '0003_auto_20211028_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectConsentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consent_file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='consents.consentfile')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subjects.subject')),
            ],
        ),
    ]
