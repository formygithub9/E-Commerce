from django.urls import path
from store import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.LandingPage),
    path('index',views.index),
    path('signup',views.signup),
    path('login',views.HandleLogin),
    path('contact',views.contact),
    path('about',views.about),
    path('search',views.Search),
    path('product-details',views.Product_Details),
    path('logout',views.HandleLogout),
    path('cart',views.Cart),
    path('check-out',views.CheckOut),
    path('check-out/placeorder',views.PlaceOrder),
    path('success',views.success),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
