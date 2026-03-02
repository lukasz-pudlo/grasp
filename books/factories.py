import factory
from books.models import Book, Author, Publication, PublishingHouse, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: "user%d" % n)


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
        django_get_or_create = ("full_name")

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Faker("catch_phrase")


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        user = Publication

    author = factory.SubFactory(AuthorFactory)
