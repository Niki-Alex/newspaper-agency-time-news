from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Newspaper, Redactor


class NewspaperForm(forms.ModelForm):
    publishers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Newspaper
        fields = "__all__"


class RedactorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "years_of_experience",
            "first_name",
            "last_name",
        )


class RedactorUpdateExperienceForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["years_of_experience"]


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False
    )


class TopicSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False
    )


class NewspaperSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False
    )
