# Generated by Django 3.1.7 on 2021-04-11 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fetch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('queued_at', models.DateTimeField(auto_now_add=True, help_text='When the fetch was queued.')),
                ('started_at', models.DateTimeField(help_text='When the fetch started.', null=True)),
                ('finished_at', models.DateTimeField(help_text='When the fetch finished.', null=True)),
                ('success', models.BooleanField(help_text='Whether the fetch succeeded.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(help_text='SHA-256 hash of file', max_length=64, unique=True)),
                ('file_type', models.CharField(choices=[('M', 'Module'), ('P', 'Project')], help_text='Type of file, if known.', max_length=1, null=True)),
                ('size', models.IntegerField(help_text='Size of file in bytes.')),
                ('cached_at', models.DateTimeField(help_text='When the file was cached.')),
                ('last_accessed_at', models.DateTimeField(help_text='When the file was last accessed.')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of this project.', max_length=500)),
                ('file', models.OneToOneField(help_text='File containing the content of this project.', on_delete=django.db.models.deletion.CASCADE, related_name='project', to='repo.file')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of this module.', max_length=500)),
                ('file', models.OneToOneField(help_text='File containing the content of this module.', on_delete=django.db.models.deletion.CASCADE, related_name='module', to='repo.file')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(help_text='URL where resource can be publicly accessed.', max_length=2048)),
                ('added_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp of when the location was added.')),
                ('added_by', models.ForeignKey(help_text='User who added the resource.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations_added', to=settings.AUTH_USER_MODEL)),
                ('last_good_fetch', models.ForeignKey(help_text='Most recent fetch that succeeded.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='repo.fetch')),
                ('most_recent_file', models.ForeignKey(help_text='File ', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locations', to='repo.file')),
            ],
        ),
        migrations.AddField(
            model_name='fetch',
            name='file',
            field=models.ForeignKey(help_text='File that was fetched, when finished, if successful.', null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='fetches', to='repo.file'),
        ),
        migrations.AddField(
            model_name='fetch',
            name='location',
            field=models.ForeignKey(help_text='Location that we are fetching.', on_delete=django.db.models.deletion.CASCADE, related_name='fetches', to='repo.location'),
        ),
    ]
