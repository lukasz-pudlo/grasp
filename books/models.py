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
    edition = models.IntegerField(blank=True, null=True)
    authors = models.ManyToManyField(
        "Author",
        through="Publication",
        related_name='books'
    )
    reader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='books',
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status
    )
    languages = models.ManyToManyField("BookLanguage", blank=True, null=True)
    isbn = models.IntegerField(max_length=13, blank=True, null=True)
    # Add validation as described in Wikipedia: https://en.wikipedia.org/wiki/ISBN

    objects = models.Manager()
    read = BookReadManager()

    class Meta:
        ordering = ['title']
        models.Index(fields=['title'])
        unique_together = ['title', 'reader']

    def __str__(self):
        return f"{self.title} ({ordinal(self.edition)} edition)"

    def get_absolute_url(self):
        return reverse(
            'books:book-detail',
            args=[self.id]
        )

    def get_authors(self):
        return ", ".join([f"{author.first_name} {author.last_name}" for author in self.authors.all()])

    def get_languages(self):
        return ", ".join([f"{booklanguage.name}" for booklanguage in self.languages.all()])


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [["first_name", "last_name"]]

    @property
    def full_name(self):
        "Returns the author's full name"
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    # This Project Gutenberg API might prove useful:
    # https://gutendex.com/?ref=dr-pa&utm_medium=public-apis-website


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


class BookLanguage(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    language_sub_tag = models.CharField(max_length=2, blank=True)
    country_sub_tag = models.CharField(max_length=2, blank=True)

    @property
    def language_tag(self):
        "Returns the full language tag as defined by IETF"
        return f"{self.language_sub_tag}-{self.country_sub_tag}"

    # Explore the standards: https://www.rfc-editor.org/rfc/rfc5646
    # Country codes: https://www.iso.org/obp/ui/#iso:pub:PUB500001:en
    # Add choices to language and country sub tags

    def __str__(self):
        return self.language_tag
