from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import School

@login_required
def school_dashboard_redirect(request):
    # Fetch schools associated with the logged-in user
    user_schools = School.objects.filter(user=request.user)

    if user_schools.count() == 1:
        # Redirect to the only school dashboard
        return redirect('school_dashboard', school_id=user_schools.first().id)
    elif user_schools.count() > 1:
        # Render a selection page if multiple schools are linked
        return render(request, 'select_school.html', {'schools': user_schools})
    else:
        # Redirect to a general page or display a message if no school is linked
        return render(request, 'no_school.html')