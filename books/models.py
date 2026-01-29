from django.db import models


class Book(models.Model):

    class Status(models.TextChoices):
        RECOMMENDED = 'RM', 'Recommended'
        STARTED = 'ST', 'Started'
        READ = 'RD', 'Read'
        ABANDONNED = 'AD', 'Abandonned'

    title = models.CharField(max_length=255)
    author = models.ManyToManyField("Author", through="Publication")

    class Meta:
        ordering = ['title']
        models.Index(fields=['title'])

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publication(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey("PublishingHouse", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'book'], name='unique_author_of_book'
            )
        ]


class PublishingHouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    established = models.DateField()
