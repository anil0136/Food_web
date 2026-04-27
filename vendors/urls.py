from django.urls import path
from vendors import views

app_name = 'vendors'

urlpatterns=[
    path('vendor_detail/<int:id>',views.vendor_details,name="vendor_detail"),
    path('vendorReg',views.VendorRegisteration,name="vendorReg"),
    path('menubuilding',views.menubuilding_details,name='menubuilding'),
    path('edit/<int:id>',views.edit_food,name='edit'),
    path('deletefood/<int:id>',views.delete_food,name="deletefood"),
    path("fran_details/<int:id>/",views.add_franchise,name="fran_details"),
    path("emi_calci/<int:id>/",views.emi,name="emi_calci")
]
