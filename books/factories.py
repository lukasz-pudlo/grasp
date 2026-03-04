from datetime import datetime
import factory
from books.models import Book, Author, Publication, PublishingHouse
from django.contrib.auth.models import User


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
    edition = factory.Faker("random_digit_not_null")
    reader = factory.SubFactory(UserFactory)
    status = factory.Faker(
        "random_element",
        elements=[
            x[0] for x in Book.Status
        ]
    )
    isbn = factory.Faker("random_number", digits=13)

    @factory.post_generation
    def languages(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.languages.add(*extracted)


class PublishingHouseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PublishingHouse

    country = factory.Iterator(["PL", "UK"])
    name = factory.Faker("company")
    address = factory.Faker("address")
    established = factory.Faker(
        "date_between",
        start_date=datetime(year=1900, month=1, day=1),
        end_date=datetime.now().date()
    )


class PublicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publication

    author = factory.SubFactory(AuthorFactory)
    book = factory.SubFactory(BookFactory)
    publisher = factory.SubFactory(PublishingHouseFactory)


class BookLanguageFactory(factory.django.DjangoModelFactory):
    name = factory.Iterator(
        ["British English", "American English", "Spanish (Spain)", "French (France)"])
    # How to make the tag correspond to the name, e.g. en-GB for British English?
