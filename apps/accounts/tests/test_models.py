from apps.accounts.models import User
from django.test import TestCase


class UserModelTest(TestCase):
    def test_create_user(self):

        test_user = User.objects.create(
            email="user@test.com",
            username="user",
            password="1234",
            first_name="userfn",
            last_name="userln",
            is_superuser=False,
            is_staff=True,
        )

        self.assertEqual(test_user.email, "user@test.com")
        self.assertEqual(test_user.username, "user")
        self.assertEqual(test_user.password, "1234")
        self.assertEqual(test_user.first_name, "userfn")
        self.assertEqual(test_user.last_name, "userln")
        self.assertTrue(test_user.is_active)
        self.assertTrue(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    def test_create_super_user(self):
        test_super_user = User.objects.create(
            email="admin@test.com",
            username="admin",
            password="1234",
            first_name="adminfn",
            last_name="adminln",
            is_superuser=True,
            is_staff=False,
        )

        self.assertEqual(test_super_user.email, "admin@test.com")
        self.assertEqual(test_super_user.username, "admin")
        self.assertEqual(test_super_user.password, "1234")
        self.assertEqual(test_super_user.first_name, "adminfn")
        self.assertEqual(test_super_user.last_name, "adminln")
        self.assertTrue(test_super_user.is_active)
        self.assertTrue(test_super_user.is_superuser)
        self.assertFalse(test_super_user.is_staff)

    def test_when_password_and_email_are_provided_the_user_is_create_as_default(self):
        test_user_default = User.objects.create(
            email="user_default@test.com",
            password="default",
        )

        self.assertEqual(test_user_default.password, "default")
        self.assertEqual(test_user_default.email, "user_default@test.com")

        self.assertEqual(test_user_default.username, "")
        self.assertEqual(test_user_default.first_name, "")
        self.assertEqual(test_user_default.last_name, "")

        self.assertTrue(test_user_default.is_active)
        self.assertTrue(test_user_default.is_staff)
        self.assertFalse(test_user_default.is_superuser)

    def test_when_isstaff_and_issuperuser_fields_are_not_provided_the_user_is_not_a_superuser(self):

        test_user_default = User.objects.create(
            email="user_default@test.com",
            password="default",
        )
        test_user_default.username = "default"
        test_user_default.last_name = "last_name_default_test"
        test_user_default.first_name = "first_name_default_test"
        test_user_default.is_active = True

        self.assertTrue(test_user_default.is_staff)
        self.assertFalse(test_user_default.is_superuser)
