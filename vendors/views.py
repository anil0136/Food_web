from django.shortcuts import render,redirect,get_object_or_404
# removed unused template loader and mark_safe import
from vendors.models import multivendors,menubuilding,Franchise,FranchiseOrder
from vendors.forms import VendorRegisterForm,VendoruserForm,MenubuildingForm,Foodupdateform
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import math

# Create your views here.
def vendor_details(request, id=0):
    vendor = multivendors.objects.get(id=id)
    allfood = menubuilding.objects.filter(ver=vendor)
    return render(request, "vendors/vendor_detail.html", {"vendor": vendor,"allfood": allfood})
    
def VendorRegisteration(request):
    registered=False
    if request.method == 'POST':
        form1 = VendoruserForm(request.POST)
        form2 = VendorRegisterForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()

            vendorprofile =form2.save(commit=False)
            vendorprofile.user=user
            vendorprofile.save()
            registered = True
            
    else:
        form1= VendoruserForm()
        form2= VendorRegisterForm()
    context={
            'form1':form1,
            'form2':form2,
            'registered': registered
        }
    return render(request,"vendors/vendorReg.html",context)

@login_required(login_url="login")
def menubuilding_details(request):
    if not hasattr(request.user, "multivendors"):
        messages.error(request, "Only vendors can add food items.")
        return redirect("dashboard")

    if request.method == 'POST':
        form1 = MenubuildingForm(request.POST, request.FILES)
        if form1.is_valid():
            food_item = form1.save(commit=False)
            # Automatically assign the vendor as the logged-in user's vendor profile
            food_item.ver = request.user.multivendors
            food_item.save()
            return redirect('dashboard')
    else:
        form1 = MenubuildingForm()

    allfood = menubuilding.objects.filter(ver=request.user.multivendors).order_by("-id")
    
    return render(request, "vendors/menubuilding.html", {'form1': form1, 'allfood': allfood})

@login_required(login_url="login")
def edit_food(request, id=0):
    if not hasattr(request.user, "multivendors"):
        messages.error(request, "Only vendors can edit food items.")
        return redirect("dashboard")
    food = get_object_or_404(menubuilding, id=id, ver=request.user.multivendors)

    if request.method == 'POST':
        form = Foodupdateform(request.POST, request.FILES, instance=food)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = Foodupdateform(instance=food)

    return render(request, 'vendors/edit_food.html', {'form': form})

@login_required(login_url="login")
def delete_food(request,id=0):
    if not hasattr(request.user, "multivendors"):
        messages.error(request, "Only vendors can delete food items.")
        return redirect("dashboard")
    fooddetails = get_object_or_404(menubuilding, id=id, ver=request.user.multivendors)
    fooddetails.delete()
    return redirect('dashboard')



@login_required(login_url="login")
def add_franchise(request, id=0):
    vendor = multivendors.objects.get(id=id)
    fran = Franchise.objects.filter(vendor=vendor).first()
    
    if request.method == 'POST':
        # Save the franchise order
        FranchiseOrder.objects.create(
            user=request.user,
            vendor=vendor,
            franchise=fran
        )
        messages.success(request, "Save Order! Your franchise proposal has been submitted successfully.")
        # Render the same franchise page so message appears in-place
        return render(request, "vendors/franchise.html", {"vendor": vendor, "fran": fran})
    
    return render(request, "vendors/franchise.html", {"vendor": vendor,"fran": fran})



def emi(request, id):
    vendor = get_object_or_404(multivendors, id=id)
    fran = get_object_or_404(Franchise, vendor=vendor)  # ✅ FIX

    emi = None
    error_message = None
    

    if request.method == "POST":
        loan_amount = float(request.POST.get("loan_amount"))
        years = int(request.POST.get("loan_years"))

        interest_map = {1: 13, 2: 11, 5: 10, 7: 9, 10: 8}
        annual_rate = interest_map.get(years)

        if not annual_rate:
            error_message = "Invalid loan duration"
        elif loan_amount > fran.total_investment:  # ✅ FIXED LOGIC
            error_message = "Loan amount should be less than total investment"
        else:
            monthly_rate = annual_rate / (12 * 100)
            months = years * 12

            emi = (
                loan_amount
                * monthly_rate
                * math.pow(1 + monthly_rate, months)
            ) / (math.pow(1 + monthly_rate, months) - 1)

    return render(
        request,
        "vendors/emi_calci.html",
        {
            "vendor": vendor,
            "fran": fran,
            "emi": emi,
            "error_message": error_message,
        },
    )
         
    

    
