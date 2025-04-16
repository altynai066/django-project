from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        # Обновляем модель Entry
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(
                    on_delete=models.SET_NULL, null=True, blank=True, to='tasks.Category')
                ),  # Добавляем связь с моделью Category
                ('priority', models.CharField(choices=[('High', 'Высокий'), ('Medium', 'Средний'), ('Low', 'Низкий')], default='Medium', max_length=10)),
                ('status', models.CharField(choices=[('Draft', 'Черновик'), ('Published', 'Опубликовано')], default='Draft', max_length=20)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        # Если была старая модель Task, её можно удалить, если она уже не нужна
        # migrations.DeleteModel(
        #     name='Task',
        # ),
    ]
