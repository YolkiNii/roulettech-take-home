from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    pub_date = models.DateTimeField("date published")

    def __str__(self) -> str:
        return self.content
