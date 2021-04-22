from typing import Any, Dict

from actstream import action
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Model
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, ListView

from ..tags.models import Tag
from ..verbs import Verb
from . import models as m


class LocationsSubmitView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = m.Location
    fields = ["url"]
    success_message = _("URL successfully submitted")
    template_name = "repo/location_submit.html"

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super(LocationsSubmitView, self).form_valid(form)

    def get_success_url(self) -> str:
        return reverse("repo:location-submit")


location_submit_view = LocationsSubmitView.as_view()


class ModulesListView(ListView):

    model = m.Module


module_list_view = ModulesListView.as_view()


class GetByHashMixin:
    model: Model
    kwargs: Dict[str, Any]

    def get_object(self, queryset=None):
        return self.model.objects.get(file__hash=self.kwargs.get("hash"))


class ModulesDetailView(GetByHashMixin, DetailView):

    model = m.Module


module_detail_view = ModulesDetailView.as_view()


class ProjectsListView(ListView):

    model = m.Project


project_list_view = ProjectsListView.as_view()


class ProjectsDetailView(GetByHashMixin, DetailView):

    model = m.Project


project_detail_view = ProjectsDetailView.as_view()


def module_add_tag_view(request, hash):
    if not request.user.is_authenticated:
        return redirect("repo:module-detail", hash=hash)
    module = get_object_or_404(m.Module, file__hash=hash)
    tags = request.POST["tags"]
    tags = tags.split(",")
    tags = [t.strip().lower() for t in tags]
    tags = [t[1:] if t[0:1] == "#" else t for t in tags]
    tags = {t for t in tags if t}
    existing_tags = {t.name for t in module.tags.all()}
    new_tags = tags - existing_tags
    for new_tag in new_tags:
        module.tags.add(new_tag)
        action.send(
            request.user,
            verb=Verb.ADDED_TAG,
            action_object=Tag.objects.get(name=new_tag),
            target=module,
        )
    count = len(new_tags)
    messages.add_message(
        request,
        messages.INFO,
        f"Added {count} new tag{'s' if count != 1 else ''}",
    )
    return redirect("repo:module-detail", hash=hash)


def project_add_tag_view(request, hash):
    if not request.user.is_authenticated:
        return redirect("repo:project-detail", hash=hash)
    project = get_object_or_404(m.Project, file__hash=hash)
    tags = request.POST["tags"]
    tags = tags.split(",")
    tags = [t.strip().lower() for t in tags]
    tags = [t[1:] if t[0:1] == "#" else t for t in tags]
    tags = {t for t in tags if t}
    existing_tags = {t.name for t in project.tags.all()}
    new_tags = tags - existing_tags
    for new_tag in new_tags:
        project.tags.add(new_tag)
        action.send(
            request.user,
            verb=Verb.ADDED_TAG,
            action_object=Tag.objects.get(name=new_tag),
            target=project,
        )
    count = len(new_tags)
    messages.add_message(
        request,
        messages.INFO,
        f"Added {count} new tag{'s' if count != 1 else ''}",
    )
    return redirect("repo:project-detail", hash=hash)
