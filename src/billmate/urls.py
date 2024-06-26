"""
URL configuration for bill project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include(('bill_group.urls', 'bill_group'), namespace='bill_group')),
    path("participant/", include(('participant.urls', 'participant'), namespace='participant')),
    path("transaction/", include(('transaction.urls', 'transaction'), namespace='transaction')),
    path("home/", include(('home.urls', 'home'), namespace='home')),
    path("accounts/", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
]
