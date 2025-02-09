from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.views.generic import CreateView, ListView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import PasswordChangeForm
from django_filters.views import FilterView
from django.views.generic import ListView, CreateView, DeleteView
from .models import CollegeAndUniversities
from django.urls import reverse_lazy
from .forms import CollegeAndUniversitiesForm



def college_list_view(request):
    colleges = CollegeAndUniversities.objects.all().order_by("-upload_time")
    return render(request, "college/college_list.html", {"colleges": colleges})


def college_add_view(request):
    if request.method == "POST":
        form = CollegeAndUniversitiesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "College/University added successfully.")
            return redirect("college_list")
    else:
        form = CollegeAndUniversitiesForm()
    return render(request, "college/college_form.html", {"form": form})


def college_update_view(request, pk):
    college = get_object_or_404(CollegeAndUniversities, pk=pk)
    if request.method == "POST":
        form = CollegeAndUniversitiesForm(request.POST, request.FILES, instance=college)
        if form.is_valid():
            form.save()
            messages.success(request, "College/University updated successfully.")
            return redirect("college_list")
    else:
        form = CollegeAndUniversitiesForm(instance=college)
    return render(request, "college/college_form.html", {"form": form})


def college_delete_view(request, pk):
    college = get_object_or_404(CollegeAndUniversities, pk=pk)
    college.delete()
    messages.success(request, "College/University deleted successfully.")
    return redirect("college_list")
