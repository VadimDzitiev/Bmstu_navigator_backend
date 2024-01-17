# Generated by Django 4.2.7 on 2024-01-07 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu', '0014_alter_request_moderator'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request',
            name='created_date',
        ),
        migrations.AddField(
            model_name='request',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='completion_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='formation_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='request',
            name='moderator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_moderator_set', to='bmstu.userprofile'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[(1, 'Черновик'), (2, 'Удален'), (3, 'Сформирован'), (4, 'Завершен'), (5, 'Отклонен')], default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='request_user_set', to='bmstu.userprofile'),
        ),
        migrations.AlterField(
            model_name='requestservice',
            name='request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmstu.request'),
        ),
        migrations.AlterField(
            model_name='requestservice',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bmstu.service'),
        ),
        migrations.AlterField(
            model_name='service',
            name='buildings',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='transition',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='transition_time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='is_moderator',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='userpassword',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterModelTable(
            name='userprofile',
            table='UserProfile',
        ),
    ]
