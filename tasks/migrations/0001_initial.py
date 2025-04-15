from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',  # Название модели Entry
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),  # Поле description вместо content
                ('priority', models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])),
                ('status', models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])),
                ('category', models.CharField(max_length=50, choices=[('Work', 'Work'), ('Personal', 'Personal')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
