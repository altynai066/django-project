from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_entry_options_rename_content_entry_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='category',
            field=models.CharField(choices=[('Work', 'Work'), ('Personal', 'Personal')], default='Personal', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')]),
        ),
        migrations.AlterField(
            model_name='entry',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], max_length=50),
        ),
    ]

