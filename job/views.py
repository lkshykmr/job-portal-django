from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Job, SavedJob
from .forms import ApplicationForm, RegisterForm



def home(request):
    return render(request, "home.html")


def job(request):
    query = request.GET.get("q")

    if query:
        jobs = Job.objects.filter(
            title__icontains=query
        )
    else:
        jobs = Job.objects.all()

    return render(
        request,
        "job.html",
        {
            "jobs": jobs
        }
    )


def job_detail(request, id):
    job = Job.objects.get(id=id)

    return render(
        request,
        "job_detail.html",
        {
            "job": job
        }
    )


@login_required
def apply_job(request, id):
    job = Job.objects.get(id=id)

    if request.method == "POST":
        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            application = form.save(
                commit=False
            )

            application.job = job
            application.user = request.user

            application.save()

            return redirect("job")

    else:
        form = ApplicationForm()

    return render(
        request,
        "apply_job.html",
        {
            "form": form,
            "job": job
        }
    )


def register(request):
    if request.method == "POST":
        form = RegisterForm(
            request.POST
        )

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data[
                    "username"
                ],
                email=form.cleaned_data[
                    "email"
                ],
                password=form.cleaned_data[
                    "password"
                ]
            )

            login(
                request,
                user
            )

            return redirect("job")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form
        }
    )


def login_view(request):
    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(
                request,
                user
            )

            return redirect("job")

    return render(
        request,
        "login.html"
    )


def logout_view(request):
    logout(request)

    return redirect("home")

@login_required
def saved_job(request, id):
    job = get_object_or_404(Job, id=id)

    SavedJob.objects.get_or_create(
        job=job,
        user=request.user
    )

    return redirect("job")