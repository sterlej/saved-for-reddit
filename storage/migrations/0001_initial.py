# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-31 21:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocalIdentity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='RedditProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reddit_user_id', models.TextField(db_index=True, null=True, unique=True)),
                ('username', models.TextField(null=True, unique=True)),
                ('refresh_token', models.CharField(max_length=200, null=True)),
                ('active', models.BooleanField(default=True)),
                ('identity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storage.LocalIdentity')),
            ],
        ),
        migrations.CreateModel(
            name='Savable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_flair_text', models.TextField(blank=True, null=True)),
                ('score', models.IntegerField(blank=True, null=True)),
                ('created_utc', models.DateTimeField(db_index=True)),
                ('date_saved', models.DateTimeField(db_index=True, null=True)),
                ('author', models.TextField(null=True)),
                ('author_user_id', models.TextField(db_index=True, null=True, unique=True)),
                ('saved_by', models.ManyToManyField(related_name='savable_set', to='storage.RedditProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('subreddit_id', models.TextField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.TextField(db_index=True)),
            ],
        ),
        migrations.AddField(
            model_name='savable',
            name='subreddit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='storage.Subreddit'),
        ),
    ]
