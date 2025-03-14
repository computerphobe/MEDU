# Generated by Django 3.1.13 on 2025-02-27 07:01

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('course', models.TextField(blank=True, max_length=3000, null=True)),
                ('fees', models.TextField(blank=True, max_length=5000, null=True)),
                ('eligibility', models.TextField(blank=True, null=True)),
                ('application_date', models.CharField(blank=True, max_length=5000, null=True)),
                ('about', models.TextField(blank=True, null=True)),
                ('highlights', models.TextField(blank=True, null=True)),
                ('departments', models.TextField(blank=True, null=True)),
                ('collaborations', models.TextField(blank=True, null=True)),
                ('ratings', models.CharField(blank=True, max_length=50, null=True)),
                ('stream', models.TextField(blank=True, max_length=255, null=True)),
                ('students_placed', models.TextField(blank=True, max_length=50, null=True)),
                ('air_rank', models.CharField(blank=True, max_length=50, null=True)),
                ('percentage_marks', models.CharField(blank=True, max_length=50, null=True)),
                ('class_xii_marks', models.CharField(blank=True, max_length=50, null=True)),
                ('type_of_course', models.CharField(blank=True, choices=[('En', 'Engineering'), ('Me', 'Medical'), ('Ma', 'Management'), ('Ar', 'Architecture'), ('La', 'Law'), ('Co', 'Commerce'), ('Sc', 'Science'), ('Ar', 'Arts'), ('Ot', 'Other')], max_length=2, null=True)),
                ('national_ranking', models.CharField(blank=True, max_length=255, null=True)),
                ('global_ranking', models.CharField(blank=True, max_length=50, null=True)),
                ('number_of_students', models.CharField(blank=True, max_length=50, null=True)),
                ('number_of_courses', models.CharField(blank=True, max_length=50, null=True)),
                ('scholarships', models.TextField(blank=True, max_length=5000, null=True)),
                ('bank_loan', models.TextField(blank=True, max_length=50, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
                ('entrance_exam', models.CharField(blank=True, max_length=50, null=True)),
                ('counselling', models.CharField(blank=True, max_length=100, null=True)),
                ('number_of_seats', models.CharField(blank=True, max_length=50, null=True)),
                ('round_1_closing_cutoff', models.CharField(blank=True, max_length=50, null=True)),
                ('general', models.CharField(blank=True, max_length=50, null=True)),
                ('obc', models.CharField(blank=True, max_length=50, null=True)),
                ('sc', models.CharField(blank=True, max_length=50, null=True)),
                ('st', models.CharField(blank=True, max_length=50, null=True)),
                ('cutoff_rounds', models.CharField(blank=True, max_length=50, null=True)),
                ('round_1_rank', models.CharField(blank=True, max_length=50, null=True)),
                ('affiliations', models.TextField(blank=True, null=True)),
                ('naac_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('application_form', models.CharField(blank=True, max_length=255, null=True)),
                ('scholarship_criteria', models.TextField(blank=True, null=True)),
                ('scholarship_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('eligibility_criteria', models.TextField(blank=True, null=True)),
                ('selection_criteria', models.TextField(blank=True, max_length=25500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='meduv1.university')),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=255)),
                ('statement_of_purpose', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('university', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='meduv1.university')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
