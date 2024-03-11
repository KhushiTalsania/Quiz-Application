# Generated by Django 4.2.10 on 2024-03-11 07:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(blank=True, default=0, max_length=6, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default=None, max_length=20, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.BigIntegerField(blank=True, null=True)),
                ('address', models.TextField(blank=True, max_length=300, null=True)),
                ('experience', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.TextField(unique=True)),
                ('options', models.JSONField(blank=True, default=dict)),
                ('answer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Outcome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default=0, max_length=100)),
                ('mark', models.IntegerField(blank=True, default=0)),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.participant')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.question')),
            ],
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.CharField(default=None, max_length=6, unique=True)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.department')),
                ('question', models.ManyToManyField(blank=True, to='projects.question')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.IntegerField(blank=True, default=0)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.exam')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.participant')),
            ],
            options={
                'unique_together': {('participant', 'exam')},
            },
        ),
    ]