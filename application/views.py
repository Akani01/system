from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User 
from django.template.loader import render_to_string, get_template 
from django.urls import reverse_lazy, reverse
from .models import Application, University
from django.contrib.auth.decorators import login_required
# Create your views here.
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
def addApplication(request):
    user = request.user
    universitys = user.university_set.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')  # Get the main image

        if data['university'] != 'none':
            university = University.objects.get(id=data['university'])
        elif data['university_new'] != '':
            university, created = University.objects.get_or_create(
                user=user,
                name=data['university_new'])
        else:
            university = None
       
        # Check if the main image is provided before creating the Application instance
        if image:
            application = Application.objects.create(
                author=user,  # Set the author to the logged-in user
                university=university,
                #next of keen
                keen=data['keen'],
                image=image,  # Use the main image
                #student
                student=data.get('student', ''),
                #address
                address=data.get('address', ''),
                #disability
                disability=data.get('disability', ''),
                #varsity
                varsity=data.get('varsity', ''),
                #bursary
                bursary=data.get('bursary', ''),
                #details
                details=data.get('details', ''),
                
            )

            # Send email to the user after successful application addition
            email_address = user.email
            subject = 'Application Added Successfully'
            listview_url = "https://www.macrosecond.com/application/listview/"
            message = (
                'Thank you for adding an application request. Your submission was successful. '
                'Will process your applications within 48 hours and you will receive a confirmation, GO AHEAD AND UPLOAD DOCUMENTS:\n\n{}'
            ).format(listview_url)
            
            context = {'name': user.first_name, 'message': message}
            email_template = get_template('emailapp/email.html').render(context)

            # Use from_email and to parameters for sender and recipient
            email = EmailMessage(subject, email_template, from_email="Macrosecond Apply <your@email.com>", to=[email_address])
            email.content_subtype = "html"
            email.send()

            return redirect('upload')  # Make sure the URL name is correct
        else:
            error_message = "Please upload the main image."
            context = {'universitys': universitys, 'error_message': error_message}
            return render(request, 'applications/addapplication.html', context)

    context = {'universitys': universitys}
    return render(request, 'applications/addapplication.html', context)

 
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