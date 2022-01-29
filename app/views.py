from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from project import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from.models import table


# Create your views here.
def home(request):
    if 'usercookie' in request.COOKIES:
        if 'username' in request.session:
            ok = val().first_name
            return render(request, "authentication/profile_dashboard.html",{"fname": ok})
        else:
            return redirect(display)
    else:
        return redirect(display)
def display(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        use2 = request.POST['username']
        fname = request.POST['fname']
        fname2 = request.POST['fname']
        lname = request.POST['lname']
        lname2 = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

        t = table(username2= use2, firstn= fname2, secondn= lname2)
        t.save()
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request,
                         "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")

        # Welcome Email
        subject = "Welcome to Rashid's project- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Rashid's website!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nRashid"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Rashid's project - Django Login!!"
        message2 = render_to_string('email_confirmation.html', {

            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        #myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return HttpResponse('Activation link is invalid!')

def signin(request):
    if 'username' in request.session:
        return redirect('home')
    elif request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            #fname = user.first_name
            global val
            def val():
                return user
            #messages.success(request, "Logged In Sucessfully!!")
            request.session['username'] = user.username
            # return render(request, "authentication/profile_dashboard.html", {"fname": fname})
            response = redirect('home')
            response.set_cookie('usercookie', max_age=3600)
            return response
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('display')

    return render(request, "authentication/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

# def port(request):
#
#     fname = user.last_name
#     return render(request, "portfolio/portfolio.html", {"fname": fname})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    global ipad
    def ipad():
        return ip
    return render(request,'authentication/profile_dashboard.html',{'ip':ip})