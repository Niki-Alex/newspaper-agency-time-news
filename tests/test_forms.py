from django.test import TestCase

from catalog.forms import RedactorCreationForm


class FormsTest(TestCase):
    def test_redactor_creat_with_years_of_experience_first_and_last_name(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "years_of_experience": 5,
            "first_name": "Sarah",
            "last_name": "Kerigan",
        }
        form = RedactorCreationForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data, form_data)

    def test_validate_years_of_experience_with_negative_numbers(self):
        form_data = {
            "username": "nova",
            "password1": "nova123456",
            "password2": "nova123456",
            "years_of_experience": -15,
        }
        form = RedactorCreationForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
        self.assertIn(
            "Years of experience cannot be negative!",
            form.errors["years_of_experience"]
        )
