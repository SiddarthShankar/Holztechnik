from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('increase-font-size/', views.increase_font_size, name='increase_font_size'),
    path('decrease-font-size/', views.decrease_font_size, name='decrease_font_size'),
    path('switch-theme/<str:theme_name>/', views.switch_theme, name='switch_theme'),
    path('order/', views.order, name='order'),
    path('customer/<int:pk>', views.customer_record, name='customer'),
    path('delete_CustomerDetails/<int:pk>', views.delete_CustomerDetails, name='delete_CustomerDetails'),
    path('add_CustomerDetails/', views.add_CustomerDetails, name='add_CustomerDetails'),
    path('update_CustomerDetails/<int:pk>', views.update_CustomerDetails, name='update_CustomerDetails'),
    path('add_OrderDetails/', views.add_OrderDetails, name='add_OrderDetails')
    
]