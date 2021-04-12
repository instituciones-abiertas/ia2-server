from factory.django import DjangoModelFactory
from apps.accounts.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = "a username"
    email = "test@email.com"
    first_name = "a first name"
    last_name = "a last name"
    is_active = True
    is_staff = True
    is_superuser = True
