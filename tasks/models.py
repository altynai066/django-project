from django.db import models

class Entry(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    category = models.CharField(max_length=50, choices=[('Work', 'Work'), ('Personal', 'Personal')])
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title
