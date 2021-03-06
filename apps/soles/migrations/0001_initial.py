# Generated by Django 2.0.8 on 2018-10-22 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoe_brand', models.CharField(max_length=120)),
                ('shoe_model', models.CharField(max_length=120)),
                ('post_pic', models.ImageField(blank=True, null=True, upload_to='media')),
                ('purchase_link', models.TextField(blank=True, null=True)),
                ('life_span', models.IntegerField()),
                ('content', models.TextField()),
                ('recommend', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('user_name', models.CharField(max_length=200)),
                ('fav_skater', models.CharField(blank=True, max_length=200, null=True)),
                ('fav_shoe', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('prof_pic', models.ImageField(blank=True, null=True, upload_to='media')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='user_post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_user_post', to='soles.User'),
        ),
    ]
