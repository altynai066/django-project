from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_auto_20250416_1001'),  # Замените на актуальную зависимость
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='category',
            field=models.ForeignKey(
                on_delete=models.SET_NULL,
                null=True,
                blank=True,
                to='tasks.Category'
            ),
        ),
    ]
