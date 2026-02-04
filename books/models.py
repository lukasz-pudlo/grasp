from django.db import models
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import ordinal
from django.urls import reverse


class BookReadManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Book.Status.READ)
        )


class Book(models.Model):

    class Status(models.TextChoices):
        RECOMMENDED = 'RM', 'Recommended'
        STARTED = 'ST', 'Started'
        READ = 'RD', 'Read'
        ABANDONNED = 'AD', 'Abandonned'
        REREADING = 'RR', 'Rereading'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    edition = models.IntegerField()
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

    objects = models.Manager()
    read = BookReadManager()

    class Meta:
        ordering = ['title']
        models.Index(fields=['title'])

    def __str__(self):
        return f"{self.title} ({ordinal(self.edition)} edition)"

    def get_absolute_url(self):
        return reverse(
            'books:book_detail',
            args=[self.id]
        )


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


class PublishingHouseQuerySet(models.QuerySet):
    def poland(self):
        return self.filter(country='PL')

    def uk(self):
        return self.filter(country='UK')


class PublishingHouse(models.Model):
    class Country(models.TextChoices):
        POLAND = 'PL', 'Poland',
        UNITED_KINGDOM = 'UK', 'United Kingdom',

    name = models.CharField(max_length=255)
    address = models.CharField(blank=True)
    country = models.CharField(
        max_length=2,
        choices=Country
    )
    established = models.DateField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    from_country = PublishingHouseQuerySet.as_manager()

    def __str__(self):
        return self.name
