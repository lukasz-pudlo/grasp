from django.db import models
from django.conf import settings


class Book(models.Model):

    class Status(models.TextChoices):
        RECOMMENDED = 'RM', 'Recommended'
        STARTED = 'ST', 'Started'
        READ = 'RD', 'Read'
        ABANDONNED = 'AD', 'Abandonned'
        REREADING = 'RR', 'Rereading'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ManyToManyField(
        "Author",
        through="Publication",
        related_name='books'
    )
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status
    )

    class Meta:
        ordering = ['title']
        models.Index(fields=['title'])

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publication(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='publications'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    publisher = models.ForeignKey("PublishingHouse",
                                  on_delete=models.CASCADE,
                                  related_name='publications'
                                  )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'book'], name='unique_author_of_book'
            )
        ]


class PublishingHouse(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField(blank=True)
    established = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
