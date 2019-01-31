# Generated by Django 2.1.5 on 2019-01-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True,null=False)),
                ('password', models.CharField(max_length=32,null=False)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('sex', models.CharField(choices=[('male', '男'), ('female', '女'), ('unknown', '未设置')], default='未选择', max_length=32)),
                ('c_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['c_time'],
            },
        ),
    ]
