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
from .models import Bursary
from django.urls import reverse_lazy
from .forms import BursaryForm

#Bursary Functions

def bursary_list_view(request):
    """Show list of all bursaries"""
    bursaries = Bursary.objects.all().order_by("-upload_time")
    return render(request, "bursary/bursary_list.html", {"bursaries": bursaries})


def bursary_add_view(request):
    """Add a new bursary"""
    if request.method == "POST":
        form = BursaryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Bursary added successfully.")
            return redirect("bursary_list")
    else:
        form = BursaryForm()
    return render(request, "bursary/bursary_add.html", {"form": form})


def bursary_update_view(request, pk):
    """Update an existing bursary"""
    bursary = get_object_or_404(Bursary, pk=pk)
    if request.method == "POST":
        form = BursaryForm(request.POST, request.FILES, instance=bursary)
        if form.is_valid():
            form.save()
            messages.success(request, "Bursary updated successfully.")
            return redirect("bursary_list")
    else:
        form = BursaryForm(instance=bursary)
    return render(request, "bursary/bursary_add.html", {"form": form})


def bursary_delete_view(request, pk):
    """Delete a bursary"""
    bursary = get_object_or_404(Bursary, pk=pk)
    bursary.delete()
    messages.success(request, "Bursary successfully deleted.")
    return redirect("bursary_list")