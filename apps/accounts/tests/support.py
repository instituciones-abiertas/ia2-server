from apps.accounts.tests.factories import UserFactory


def create_and_login_user(client, *, password="password", **kargs):
    user = UserFactory.create(**kargs)
    user.set_password(password)
    user.save()
    client.login(username=user.get_username(), password=password)
    return user
