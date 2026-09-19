from django.shortcuts import get_object_or_404, render,redirect
from shoppingapp.forms import registrationForm,login_form,forgetpass,requestotp,completeorderform,updateprofileform
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse ,JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User 
from shoppingapp.models import Cart, Wishlist, completeorder, section ,product,detailing
from django.views.generic import ListView,DetailView,TemplateView
from django.contrib import messages  # make sure this import is there
from django.core.mail import send_mail
from django.conf import settings
import logging
import random
import stripe
from django.views.decorators.csrf import csrf_exempt

# <<< NEW: Stripe API key setup

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

# Create your views here.


def random_numbers():
    return random.randint(1000,9999)


def home(request):
    section_display=section.objects.all()
    if request.method =='POST':
        # The contact form uses the sender's account email, so visitors must log in first
        if not request.user.is_authenticated:
            return redirect('login')
        subjects=request.POST.get('subject')
        messages=request.POST.get('message')
        username=request.user.username 
        email=request.user.email
        subject=subjects

        message=f'{messages} , message has been sent by user - {username} his/her email id is {email}'
      
        from_email = settings.EMAIL_HOST_USER  
        print(from_email)
        recipient_list = ["officialzyanya@gmail.com"]
        send_mail(subject, message, from_email, recipient_list ,fail_silently=True)
           

    return render (request,'home.html',{'section_display':section_display})

def regiter(request):
    if request.method =='POST':
        form=registrationForm(request.POST)
        if form.is_valid():
           
            email=form.cleaned_data['email']
        
            username=form.cleaned_data['username']
            request.session['username']=username
            site=request.build_absolute_uri('/validation/')
            request.session['pending_email'] = email
            # A fresh OTP per registration, kept in the session so every server worker can check it
            random_value = random_numbers()
            request.session['otp'] = str(random_value)
           
            form.save()
            
            
            subject = "Welcome to Zyanya 🎉"
            message = f"Hi {username},\n\nThank you for registering with us! \n your otp is {random_value} this otp is valid for 2 minutes\n click here {site}  to verify your otp  "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            try:
                send_mail(subject, message, from_email, recipient_list)
            except Exception:
                # Don't block sign-up, but leave a trace in the server logs
                logger.exception("Could not send OTP email to %s", email)
            return redirect('validation')
        
    else:
        form=registrationForm()
    return render(request,'auth/register.html',{'form':form})



def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form=login_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            user=authenticate(request,username=username,password=password)

            if user:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse("credentials are not verified")
    else:
        form=login_form()

    return render(request,'auth/login.html',{'form':form})


def logout_view(request):
    logout(request)
    return redirect('login')

def forgetpassword(request):
    if request.method == 'POST':
        form=forgetpass(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']

            try:
                user=User.objects.get(username=username)
                user.set_password(password)
                user.save()
                return redirect('login')
            except User.DoesNotExist:
                return redirect('forgetpassword')
            
    else:
        form=forgetpass()

    return render(request,'auth/forgetpassword.html',{'form':form})

class SectionDetailView(DetailView):
    model = section
    context_object_name = 'section'
    template_name = 'products.html'

# def SectionDetailView(request,id):
#     product_id=section.objects.get(id=id)
#     return render(request,'products.html',{'product_id':product_id})

class moredetails(LoginRequiredMixin,DetailView):
    model=product
    context_object_name="product"
    template_name="moredetails.html"


@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html',{})

@login_required(login_url='login')
def updateprofile(request):
    if request.method == 'POST':
        form=updateprofileform(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=updateprofileform(instance=request.user)

    return render(request,'auth/updateprofile.html',{'form':form})

# @login_required(login_url='login')
# def about(request):
#     phone=request.session.get('pending_phone')
#     return render(request,'about.html',{'phone':phone})

class about(LoginRequiredMixin,TemplateView):
    template_name='about.html'


#todo  >>>>>>>>>>>>>>>>>>   add to cart code   >>>>>>>>>>>>>>>>>

#! add , subtract, delete
@login_required(login_url='login')
def add_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required(login_url='login')
def subtract_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # delete if quantity goes below 1
    return redirect('cart')

@login_required(login_url='login')
def remove_item(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')


#! add to cart

@login_required(login_url='login')
def add_to_cart(request, id):
    product_instance = get_object_or_404(product, id=id)

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product_instance)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product_instance.product_name} added to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'home'))  # stay on same page

#! cart  

@login_required(login_url='login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price,})



#! other data
def validation(request):
    pending_email = request.session.get('pending_email')  
    if request.method =='POST':
        form=requestotp(request.POST)
        if form.is_valid():
            otp=form.cleaned_data.get('otp')
           
            if otp == request.session.get('otp'):
                request.session.pop('otp', None)
                return redirect('login')
            else:
                return HttpResponse("otp is not verified")
    else:
        pending_email = request.session.get('pending_email')  
        form=requestotp()

    return render(request,'auth/validation.html',{'form':form,'pending_email':pending_email})

@login_required(login_url='login')
def checkout(request):
    # <<< MODIFIED: Only render checkout page; do not save order here
    form = completeorderform(instance=request.user)
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.product_price * item.quantity for item in cart_items)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form,
         'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLIC_KEY, 
    })


# <<< NEW: Stripe PaymentIntent view (unchanged)
@login_required(login_url='login')
@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.product_price * item.quantity for item in cart_items)
        amount = int(total_price * 100)  # Stripe expects amount in paise

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='inr',
            )
            return JsonResponse({'client_secret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'error': str(e)})


# <<< NEW: Save order only after successful payment
@login_required
@csrf_exempt
def confirm_payment(request):
    if request.method == "POST":
        form = completeorderform(request.POST)
        print("📦 POST DATA:", request.POST)  # <--- ADD THIS LINE
        print("📋 Form Errors:", form.errors)  # <--- ADD THIS LINE

        username=form.cleaned_data.get('username')
        email=form.cleaned_data.get('email')


        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user 
            order.username = request.user.username       # ✅ auto fill username
            order.email = request.user.email            # ✅ auto fill email from logged-in user
            order.save()

            # ✅ clear cart
            Cart.objects.filter(user=request.user).delete()

            # ✅ send email
            subject = "Order placed successfully 🎉"
            message =f"""Hi {username},

                    Thank you for shopping with us! 🙏  
                    Your order has been placed successfully 
                    and is now being processed.  

                    We'll keep notifying you on your email id 
                    {email}.  
                  
                    If you have any questions, feel free to reach 
                    out to our support team.  

                    Best regards,  
                    Team Zyanya
                             """
            send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email], fail_silently=False)

            return JsonResponse({"success": True})
        else:
            return JsonResponse({"error": "Form invalid", "details": form.errors})
    return JsonResponse({"error": "Invalid request"}, status=400)



@login_required(login_url='login')
def orderplaced(request):
    return render(request,'placed.html',{})

@login_required(login_url='login')
def add_to_wishlist(request, id):
    products = get_object_or_404(product, id=id)
    Wishlist.objects.get_or_create(user=request.user, product=products)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required(login_url='login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required(login_url='login')
def remove_from_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id, user=request.user)
    item.delete()
    return redirect('wishlist')


@login_required(login_url='login')
def coupnes(request):
    return render (request,'coupnes.html',{})



