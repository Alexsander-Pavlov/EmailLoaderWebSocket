# Generated by Django 5.1.2 on 2024-10-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailscaner', '0003_email_last_index_message_sender_alter_message_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Имя сохраненного файла', max_length=245, verbose_name='имя')),
                ('file', models.FileField(blank=True, help_text='Файл из сообщения, если есть', null=True, upload_to='<django.db.models.fields.CharField>/', verbose_name='файл')),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='file',
        ),
        migrations.AddField(
            model_name='message',
            name='files',
            field=models.ManyToManyField(help_text='Сохраненые файлы', to='mailscaner.file', verbose_name='файлы'),
        ),
    ]