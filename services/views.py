from django.core.mail import send_mail
from django.http import HttpResponse
import random
from .forms import UserRegistrationForm

# def home_view1(request):
#     services = Service.objects.filter(active=True)
#     return render(request, 'home.html', {'services': services})


def send_test_email(request):
    send_mail(
        'Test Email',  # Subject
        'This is a test email from the IT Services Django project.',  # Message body
        'shalinidy2002@gmail.com',  # From email
        ['recipient@example.com'],  # To email (can be a list of recipients)
        fail_silently=False,
    )
    return HttpResponse("Email has been sent successfully!")



def generate_otp():
    return random.randint(1000, 9999)  # Generates a 4-digit random OTP

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            otp = generate_otp()  # Generate the OTP
            request.session['otp'] = otp  # Store the OTP in the session
            request.session['user_data'] = form.cleaned_data  # Store user data temporarily in the session

            # Send the OTP to the user's email
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',  # Email body with OTP
                'your_email@gmail.com',  # Sender's email
                [form.cleaned_data['email']],  # Recipient's email
                fail_silently=False,
            )
            return redirect('confirm_otp')  # Redirect to the OTP confirmation page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

from django.contrib.auth.models import User
from django.contrib import messages

def confirm_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')  # Retrieve OTP entered by the user
        stored_otp = request.session.get('otp')  # Retrieve the OTP stored in the session

        if int(entered_otp) == stored_otp:  # Check if the OTP matches
            user_data = request.session.get('user_data')  # Retrieve user data from the session
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            user.save()  # Save the user to the database
            return redirect('home')  # Redirect to the home page upon successful registration
        else:
            messages.error(request, 'Invalid OTP. Please try again.')  # Show an error message if OTP is wrong

    return render(request, 'confirm_otp.html')

from django.contrib.auth.decorators import login_required



@login_required
def home_view1(request):
    services = Service.objects.filter(active=True)
    return render(request, 'home.html', {'services': services})


from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')





from django.shortcuts import render, redirect, get_object_or_404
from .models import Service
from .forms import ServiceForm

def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')  # Redirect to a list view
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})

def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'update_service.html', {'form': form})

def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'delete_service.html', {'service': service})

def list_services(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})






import razorpay
from django.conf import settings

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def subscription_view(request, service_id):
    # Retrieve the service the user wants to subscribe to
    service = get_object_or_404(Service, id=service_id)

    # Calculate total price with tax
    total_price = service.service_price + (service.service_price * service.service_tax / 100)

    if request.method == 'POST':
        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': int(total_price * 100),  # Amount in paisa (multiply by 100 for INR)
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Pass necessary info to the template
        context = {
            'service': service,
            'total_price': total_price,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'callback_url': '/payment/callback/'
        }

        return render(request, 'payment.html', context)

    return render(request, 'subscription.html', {'service': service, 'total_price': total_price})


import razorpay
from .models import Subscription  # Import your Subscription model
from django.conf import settings

# Initialize Razorpay client with your credentials
import razorpay
from django.conf import settings

# Correct initialization, using settings values
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def payment_callback(request):
    if request.method == 'POST':
        # Fetch the Razorpay payment details from the POST data
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        # Dictionary of parameters to verify the payment signature
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify the payment signature to ensure it's valid
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If the signature is valid, update the Subscription model (save the payment details)
            Subscription.objects.create(
                order_id=order_id,
                payment_id=payment_id,
                status='SUCCESS'  # Mark payment as successful
            )

            # Redirect to the success page or show success message
            return render(request, 'payment_success.html', {'payment_id': payment_id})

        except razorpay.errors.SignatureVerificationError:
            # Handle signature verification failure
            return render(request, 'payment_failed.html')

    # If request method is not POST, redirect to home
    return redirect('home')

import razorpay

def payment_callback(request):
    if request.method == 'POST':
        # Fetch Razorpay response details
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')



        try:
            # Verify the payment signature to ensure it’s valid
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            razorpay_client.utility.verify_payment_signature(params_dict)

            # If the payment is successful, save the transaction details in the database
            Subscription.objects.create(
                order_id=order_id,
                payment_id=payment_id,
                status='SUCCESS'
            )

            return render(request, 'payment_success.html', {'payment_id': payment_id})

        except razorpay.errors.SignatureVerificationError:
            # If verification fails, redirect to the failure page
            return render(request, 'payment_failed.html')

    return redirect('home')
