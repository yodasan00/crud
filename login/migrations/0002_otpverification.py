# Generated by Django 5.1.4 on 2025-01-16 18:05

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=4, validators=[django.core.validators.RegexValidator(message='Enter a valid 4-digit OTP.', regex='^\\d{4}$')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp_verifications', to='login.userdetails')),
            ],
        ),
    ]