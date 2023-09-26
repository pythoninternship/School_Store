from django.views.decorators.cache import never_cache  # Import never_cache decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Department, Course, Purpose, Material
from django.contrib import messages, auth
from django.contrib.auth.models import User
from .forms import OrderForm
from django.http import JsonResponse

# Apply the never_cache decorator to the view functions where caching should be disabled

@never_cache
def home(request):
    departments = Department.objects.all()
    return render(request, 'home.html', {'departments': departments})

@never_cache
def read_view(request):
    return render(request, 'read_more.html')

@never_cache
def about_view(request):
    return render(request, 'about.html')


@login_required(login_url='/login/?error=1')  # Specify the login URL with the error query parameter
def dashboard_view(request):
    # Check for the error query parameter and display an error message
    if 'error' in request.GET and request.GET['error'] == '1':
        messages.error(request, 'Please log in to access the dashboard page.')

    return render(request, 'dashboard.html', {'user': request.user})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard_view')
        else:
            messages.error(request, 'Invalid credentials')

    # Check for the error query parameter and display an error message
    if 'error' in request.GET and request.GET['error'] == '1':
        messages.error(request, 'Please log in to access the order page.')

    return render(request, 'login.html')


@never_cache
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username Taken')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login_view')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'register.html')

@never_cache
def logout(request):
    auth.logout(request)
    return redirect('home')

@login_required(login_url='/login/?error=1')  # Specify the login URL with the error query parameter
def order_form_view(request):
    departments = Department.objects.all()
    purposes = Purpose.objects.all().values_list('id', 'name')
    materials = Material.objects.all().values_list('id', 'name')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Handle form submission here (e.g., save data to the database)
            confirmation_message = 'Order Confirmed'
            return render(request, 'order_form.html',
                          {'form': form, 'confirmation_message': confirmation_message, 'departments': departments,
                           'purposes': purposes, 'materials': materials})
    else:
        form = OrderForm()

    return render(request, 'order_form.html',
                  {'form': form, 'departments': departments, 'purposes': purposes, 'materials': materials})
@never_cache
def get_courses(request):
    department_id = request.GET.get('department_id')
    data = {'courses': []}  # Initialize with an empty list

    if department_id:
        courses = Course.objects.filter(department_id=department_id).values('id', 'name')
        data['courses'] = list(courses)  # Convert courses queryset to a list of dictionaries

    return JsonResponse(data)
