from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):
    def test_redactor_str(self):
        redactor = get_user_model().objects.create_user(
            username="nova",
            password="blackstar2000",
            first_name="Sarah",
            last_name="Kerigan"
        )

        self.assertEquals(
            str(redactor),
            f"{redactor.username} ({redactor.first_name} {redactor.last_name})"
        )

    def test_creat_redactor_with_license_number(self):
        username = "nova"
        password = "blackstar2000"
        years_of_experience = 7
        redactor = get_user_model().objects.create_user(
            username=username,
            password=password,
            years_of_experience=years_of_experience
        )

        self.assertEquals(redactor.username, username)
        self.assertTrue(redactor.check_password(password))
        self.assertEquals(redactor.years_of_experience, years_of_experience)
