from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin456321"
        )
        self.client.force_login(self.admin_user)
        self.redactor = get_user_model().objects.create_user(
            username="nova",
            password="nova12356",
            years_of_experience=12
        )

    def test_redactor_years_of_experience_listed(self):
        url = reverse("admin:catalog_redactor_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_detail_years_of_experience_listed(self):
        url = reverse("admin:catalog_redactor_change", args=[self.redactor.id])
        response = self.client.get(url)

        self.assertContains(response, self.redactor.years_of_experience)

    def test_redactor_add_years_of_experience_listed(self):
        url = reverse("admin:catalog_redactor_add")
        response = self.client.get(url)

        self.assertContains(response, "years_of_experience")
