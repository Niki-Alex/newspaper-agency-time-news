from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Topic, Redactor, Newspaper
# from .forms import (
#     DriverCreationForm,
#     DriverLicenseUpdateForm,
#     CarForm,
#     DriverSearchForm,
#     CarSearchForm,
#     ManufacturerSearchForm
# )


@login_required
def home_page(request):
    num_redactors = Redactor.objects.count()
    num_newspapers = Newspaper.objects.count()
    num_topics = Topic.objects.count()

    context = {
        "num_redactors": num_redactors,
        "num_newspapers": num_newspapers,
        "num_topics": num_topics,
    }

    return render(request, "newspaper/home_page.html", context=context)


class TopicListView(generic.ListView):
    model = Topic
    context_object_name = "topic_list"
    template_name = "newspaper/topics_list.html"
    paginate_by = 5


class RedactorListView(generic.ListView):
    model = Redactor
    template_name = "newspaper/redactor_list.html"
    paginate_by = 5


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = "newspaper/newspaper_list.html"
    paginate_by = 5
