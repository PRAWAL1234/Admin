"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('store/',store),
    path('store/category/<x>',category),
    path('category/<x>',category),
    path('store/category/<c_name>/<p_id>',product_details),
    path('cart/',Cart),
    path('login/',login),
    path('logout',logout),
    path('signup',signup),
    path('accounts/activate/<uid>/<token>',activate),
    path('forgot/',forgot),
    path('reset-password/<uid>/<token>',reset),
    path('reset-submit/',ResetSubmit),
    path('store/add-to-cart/<p_id>',AddCart),
    path('remove/<p_id>',remove),
    path('remove-item/<p_id>',removeItem),
    path('add-item/<p_id>',AddItem),
    path('checkout/',checkout)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
