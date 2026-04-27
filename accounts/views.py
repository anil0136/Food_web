from django.shortcuts import render,redirect
from accounts.forms import UserForm,UserDetails,UserUpdateForm,UserRegisterUpdateForm, ForgotPasswordForm, ResetPasswordForm
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from vendors.models import multivendors,menubuilding,FranchiseOrder
from cart.models import Order,OrderItem
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def user_registeration(request):
    registered=False
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = UserDetails(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            profile=form2.save(commit=False)
            profile.user = user
            profile.save()
            registered=True
    else:
        form1 = UserForm()
        form2 = UserDetails()   
    return render(request,'registeration.html',{'form1':form1 ,'form2':form2 , 'registered':registered })

def auth_choice(request):
    mode = request.GET.get("mode", "register")
    if mode not in ["register", "login"]:
        mode = "register"
    return render(request, "auth_choice.html", {"mode": mode})

def user_login(request):
    if request.method == 'POST':
            username= request.POST['username']
            password= request.POST['password']
            user = authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return redirect("dashboard" if hasattr(user, "multivendors") else "home")
            else:
                messages.error(request, "Please check your username and password.")
    return render(request,'login.html',{})

def home(request):
    allvendors=multivendors.objects.filter(is_approved=True)
    featured_food = menubuilding.objects.filter(ver__is_approved=True).select_related("ver").order_by("-id")[:12]
    return render(request,'home.html',{'allvendors':allvendors, 'featured_food': featured_food})

@login_required(login_url="login")
def user_logout(request):
    logout(request)
    return redirect("home")

@login_required(login_url="login")
def dashboard(request):
    context = {}

    # Vendor section
    if hasattr(request.user, 'multivendors'):
        vendor = request.user.multivendors
        allfood = menubuilding.objects.filter(ver=vendor)
        franchise_orders = FranchiseOrder.objects.filter(vendor=vendor).select_related('franchise').order_by('-created_at')

        # Fetch orders containing this vendor's food items
        order_items = OrderItem.objects.filter(food_item__ver=vendor).select_related(
            'order', 'order__user', 'order__user__userregister', 'food_item'
        ).order_by('-order__created_at')
        
        # Group by order
        orders_dict = {}
        for item in order_items:
            if item.order.id not in orders_dict:
                orders_dict[item.order.id] = {
                    'order': item.order,
                    'items': [],
                    'vendor_total': 0,
                }
            orders_dict[item.order.id]['items'].append(item)
            orders_dict[item.order.id]['vendor_total'] += item.price * item.qty
        
        context['vendor'] = vendor
        context['allfood'] = allfood
        context['franchise_orders'] = franchise_orders
        context['vendor_orders'] = orders_dict.values()  # list of dicts: {'order': order, 'items': [orderitem,...]}

    # User section
    if hasattr(request.user, 'userregister'):
        user_profile = request.user.userregister
        food_orders = Order.objects.filter(user=request.user).order_by('-created_at')
        context['user_profile'] = user_profile
        context['food_orders'] = food_orders

    return render(request, 'dashboard.html', context)

@login_required(login_url="login")
def update_view(request):
    form1 = UserUpdateForm(instance=request.user)
    form2 = UserRegisterUpdateForm(instance=request.user.userregister)
    if request.method=='POST':
        form1 = UserUpdateForm(request.POST,instance=request.user)
        form2 = UserRegisterUpdateForm(request.POST,request.FILES,instance=request.user.userregister)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.save()
            profile= form2.save(commit=False)
            profile.user = user
            profile.save()
            return redirect("dashboard")
    return render(request,'update.html',{'form1':form1 , 'form2':form2})


def forgot_password(request):
    form = ForgotPasswordForm(request.POST or None)
    reset_form = ResetPasswordForm(request.POST or None)
    user_obj = None

    if request.method == 'POST':
        # Validate identifier and new passwords together (single-page flow)
        if not form.is_valid() or not reset_form.is_valid():
            messages.error(request, "Please correct the highlighted fields.")
            return render(request, 'forgot_password.html', {'form': form, 'reset_form': reset_form, 'user_obj': None})

        identifier = form.cleaned_data['identifier']
        new_password = reset_form.cleaned_data['new_password']
        confirm_password = reset_form.cleaned_data['confirm_password']

        # find user by username or email (case-insensitive)
        user = User.objects.filter(username__iexact=identifier).first() or User.objects.filter(email__iexact=identifier).first()
        if not user:
            # try matching vendor by restaurant name
            from vendors.models import multivendors as VendorModel
            vendor_match = VendorModel.objects.filter(restaurant_name__iexact=identifier).first()
            if vendor_match:
                # use the vendor's user account for password reset
                user = vendor_match.user
            else:
                # no match at all — show tailored message
                if "@" in identifier:
                    messages.error(request, "No account found with that email.")
                else:
                    messages.error(request, "No user or vendor found with that username or restaurant name.")
                return render(request, 'forgot_password.html', {'form': form, 'reset_form': reset_form, 'user_obj': None})

        # show username/vendor name for clarity
        user_obj = user

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'forgot_password.html', {'form': form, 'reset_form': reset_form, 'user_obj': user_obj})

        # set password and finish
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password updated successfully. You can now log in with your new password.")
        return redirect('login')

    return render(request, 'forgot_password.html', {'form': form, 'reset_form': reset_form, 'user_obj': None})



