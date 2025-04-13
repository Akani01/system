from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User 
from django.template.loader import render_to_string, get_template 
from django.urls import reverse_lazy, reverse
from .models import Application, University
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView
from django.contrib import messages
import os

#gallery

def gallery(request):
    user = request.user
    university = request.GET.get('university')
    if university == None:
        applications = Application.objects.university(university__user=user)
    else:
        applications = Application.objects.university(
            university__name=university, university__user=user)

    universitys = University.objects.university(user=user)
    context = {'universitys': universitys, 'applications': applications}
    return render(request, 'applications/applicationgallery.html', context)



#view phot propfirms
def viewApplication(request, pk):
    application = Application.objects.get(id=pk)
    return render(request, 'applications/application.html', {'application': application})



#add application
def post_add(request):
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, request.FILES)
        title = request.POST.get("title")
        
        if form.is_valid():
            post = form.save()

            # Send email to all users
            User = get_user_model()
            all_users = User.objects.filter(is_active=True, email__isnull=False).exclude(email="")  # make sure they have emails

            subject = f'New Post: {title}'
            post_url = f"https://www.elimcircuit.com"  # Change URL to match your actual post detail view
            message = (
                f'Hello,\n\nA new post titled "{title}" has just been uploaded to our platform.\n'
                f'Check it out here: {post_url}\n\nThanks for staying connected!'
            )

            for user in all_users:
                context = {'name': user.first_name or user.username, 'message': message}
                email_template = get_template('emailapp/email.html').render(context)
                
                email = EmailMessage(
                    subject,
                    email_template,
                    from_email="CMS Notifications <elimcircuit@gmail.com>",  # or whatever your DEFAULT_FROM_EMAIL is
                    to=[user.email],
                )
                email.content_subtype = "html"
                email.send(fail_silently=True)

            messages.success(request, f"{title} has been uploaded and emails sent.")
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm()
    
    return render(
        request,
        "core/post_add.html",
        {
            "title": "Add Post",
            "form": form,
        },
    )


#galleryview
def galleryview(request):
	applications = Application.objects.all()
	context = {'applications': applications}
	template = 'applications/listview.html'	
	return render(request, template, context)

#delete gallery image
def deleteApplication(request, pk):
    applications = Application.objects.get(id=pk)
    if len(applications.image) > 0:
        os.remove(applications.image.path)
    applications.delete()
    messages.success(request,"Product Deleted Successfuly")
    return redirect('listview')

#university view
def UniversityView(request, university):
    user = request.user
    university_applications = Application.objects.university(user=user)
    return render(request, 'applications/universitys.html', { university_applications : university_applications})

#add university
def AddUniversityView(request):
    if request.method == 'POST':
        # Handle form submission to add the university to the database
        # This could involve creating a new instance of the University model
        # For simplicity, let's assume the form contains fields for university name, location, etc.
        name = request.POST.get('name')
        # Create a new University instance
        university = University.objects.create(name=name)
        # You can add more fields as needed
        return render(request, 'home.html')  # Render a success page
    else:
        return render(request, 'applications/adduniversity.html')  # Render the form for adding a university