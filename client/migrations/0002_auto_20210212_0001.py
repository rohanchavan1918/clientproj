# Generated by Django 3.1.6 on 2021-02-11 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='client',
        ),
        migrations.CreateModel(
            name='ClientProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.project')),
            ],
        ),
        migrations.AddField(
            model_name='client',
            name='projects',
            field=models.ManyToManyField(blank=True, null=True, through='client.ClientProjects', to='client.Project'),
        ),
    ]