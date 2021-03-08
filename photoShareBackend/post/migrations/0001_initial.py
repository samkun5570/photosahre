# Generated by Django 3.1.7 on 2021-03-08 16:15

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
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(editable=False, upload_to='post/%y/%m/%d')),
                ('location', models.TextField(blank=True, max_length=30, null=True, verbose_name='Post location ')),
                ('caption', models.TextField(blank=True, max_length=430, null=True, verbose_name='Post caption ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('comment_text', models.CharField(max_length=100)),
                ('comment_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to=settings.AUTH_USER_MODEL)),
                ('comment_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='post.post')),
            ],
            options={
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('like_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_likes', to=settings.AUTH_USER_MODEL)),
                ('like_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_likes', to='post.post')),
            ],
            options={
                'ordering': ['-created_on'],
                'unique_together': {('like_post', 'like_author')},
            },
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on'],
                'unique_together': {('follower', 'following')},
            },
        ),
    ]