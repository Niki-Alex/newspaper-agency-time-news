from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Topic, Redactor, Newspaper
from .forms import (
    RedactorCreationForm,
    RedactorUpdateExperienceForm,
    NewspaperForm,
    RedactorSearchForm,
    TopicSearchForm,
    NewspaperSearchForm
)


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
    paginate_by = 5
    context_object_name = "topic_list"
    template_name = "newspaper/topic_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")

        context["search_form"] = TopicSearchForm(initial={
            "name": name
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )

        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("catalog:topic-list")
    template_name = "newspaper/topic_form.html"


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("catalog:topic-list")
    template_name = "newspaper/topic_form.html"


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("catalog:topic-list")
    template_name = "newspaper/topic_confirm_delete.html"


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 5
    template_name = "newspaper/redactor_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RedactorListView, self).get_context_data(**kwargs)
        username_ = self.request.GET.get("username", "")

        context["search_form"] = RedactorSearchForm(initial={
            "username": username_
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q")

        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query)
            )

        return queryset


class RedactorTopListView(generic.ListView):
    model = Redactor
    template_name = "newspaper/redactor_top_3_list.html"


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.all().prefetch_related(
        "newspapers__topic"
    )
    template_name = "newspaper/redactor_detail.html"


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    success_url = reverse_lazy("catalog:redactor-list")
    template_name = "newspaper/redactor_form.html"


class RedactorUpdateExperienceView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateExperienceForm
    template_name = "newspaper/redactor_form.html"
    success_url = reverse_lazy("catalog:redactor-list")


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    template_name = "newspaper/redactor_confirm_delete.html"
    success_url = reverse_lazy("catalog:redactor-list")


class NewspaperListView(generic.ListView):
    model = Newspaper
    template_name = "newspaper/newspaper_list.html"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewspaperListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")

        context["search_form"] = NewspaperSearchForm(initial={
            "title": title
        })

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("q")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query)
            )

        return queryset


class NewspaperDetailView(generic.DetailView):
    model = Newspaper
    template_name = "newspaper/newspaper_detail.html"


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("catalog:newspaper-list")
    template_name = "newspaper/newspaper_form.html"


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    success_url = reverse_lazy("catalog:newspaper-list")
    template_name = "newspaper/newspaper_form.html"


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("catalog:newspaper-list")
    template_name = "newspaper/newspaper_confirm_delete.html"


@login_required
def toggle_assign_to_news(request, pk):
    redactor = Redactor.objects.get(id=request.user.id)
    if Newspaper.objects.get(id=pk) in redactor.newspapers.all():
        redactor.newspapers.remove(pk)
    else:
        redactor.newspapers.add(pk)
    return HttpResponseRedirect(reverse_lazy(
        "catalog:newspaper-detail", args=[pk])
    )
