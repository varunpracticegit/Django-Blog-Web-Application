from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextField(blank=True, null=True)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comment')
    body = models.TextField()
    name = models.CharField(max_length=70)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s ' % (self.post.title, self.name)

