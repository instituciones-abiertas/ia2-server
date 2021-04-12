from factory import Faker, LazyAttribute
from factory.django import DjangoModelFactory
from apps.accounts.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = LazyAttribute(lambda o: o.first_name.lower())
    email = LazyAttribute(lambda o: "%s@ia2.coop" % o.username)
    first_name = Faker("first_name", locale="es_ES")
    last_name = Faker("last_name", locale="es_ES")
    is_active = True
    is_staff = True
    is_superuser = True
