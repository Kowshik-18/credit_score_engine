from django.contrib import admin
from django.urls import path, include
from loan_app.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
     path('', include('loan_app.urls')),
     path('',home, name='home')

]
