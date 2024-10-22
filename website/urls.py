from django.urls import path
from django.views.i18n import set_language
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('about/', views.about, name='about'),
    path('increase-font-size/', views.increase_font_size, name='increase_font_size'),
    path('decrease-font-size/', views.decrease_font_size, name='decrease_font_size'),
    path('switch-theme/<str:theme_name>/', views.switch_theme, name='switch_theme'),
    path('order/<int:order_id>/', views.order, name='order'),
    path('customer/<int:pk>', views.customer_record, name='customer'),
    path('delete_CustomerDetails/<int:pk>', views.delete_CustomerDetails, name='delete_CustomerDetails'),
    path('add_CustomerDetails/', views.add_CustomerDetails, name='add_CustomerDetails'),
    path('update_CustomerDetails/<int:pk>', views.update_CustomerDetails, name='update_CustomerDetails'),
    path('add_OrderDetails/', views.add_OrderDetails, name='add_OrderDetails'),
    path('add_OrderSpecs/', views.add_OrderSpecs, name='add_OrderSpecs'),
    path('i18n/', set_language, name='set_language'),
    path('delete_OrderDetails/<int:pk>', views.delete_OrderDetails, name='delete_OrderDetails'),
    path('update_OrderDetails/<int:pk>', views.update_OrderDetails, name='update_OrderDetails'),
    path('update_OrderSpecs/<int:pk>', views.update_OrderSpecs, name='update_OrderSpecs'),
    path('enter_order_id/', views.enter_order_id, name='enter_order_id'),
    path('pickings/<int:order_id>/', views.picking_list, name='picking_list'),
]