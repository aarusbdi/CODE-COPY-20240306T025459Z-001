from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render
from .models import Products, CustomerOrders, SubCategories
from django.db.models import Sum


# Create your views here.


def get_sales_data():
    # Filter Products with associated CustomerOrders, and calculate total sales per seller
    sales_data = Products.objects.filter(customerorders__isnull=False) \
        .values('added_by_merchant_id__company_name') \
        .annotate(total_sales=Sum('customerorders__purchase_price')) \
        .order_by('added_by_merchant_id__company_name')
    return sales_data

def my_view(request):
    # Get total sales data for rendering in the template
    sales_data = get_sales_data()
    print(sales_data)
    return render(request, 'admin_templates/my_template.html', {'sales_data': sales_data})

def demoPage(request):
    return HttpResponse("demo Page")

def demoPageTemplate(request):
    return render(request,"demo.html")

def adminLogin(request):
    return render(request,"admin_templates/signin.html")

def adminLoginProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")

    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        login(request=request,user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request,"Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))