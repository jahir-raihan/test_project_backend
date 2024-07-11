from django.db import models


class Blog(models.Model):

    blog_title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    blog_body = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.blog_title} - {self.author}'
