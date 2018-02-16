from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r"^accounts?/login/$", views.LoginView.as_view(), name="account_login"),
    url(r"^accounts?/signup/$", views.SignupView.as_view(), name="account_signup"),
    url(r"^accounts?/password_change", auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'), name="password_change"),
    url(r"^password_change_done", auth_views.PasswordChangeView.as_view(template_name='account/password_change_done.html'), name="password_change_done"),
    url(r"^accounts?/", include("account.urls")),

    url(r'^$', views.itemList, name='itemlist'),

    url(r'^getitems$', views.getItems, name='getItems'),
    url(r'^getitemarray$', views.getItemArray, name='getItemArray'),
    url(r'^addtocart$', views.addToCart, name='addToCart'),
    url(r'^setincart$', views.setInCart, name='setInCart'),
    url(r'^getitemprices$', views.getItemPrices, name='getItemPrices'),
    url(r'^getcartsum$', views.getCartSum, name='getCartSum'),
    url(r'^getcart$', views.getCart, name='getCart'),
    url(r'^getinvocepdf$', views.getInvocePdf, name='getInvocePdf'),
    url(r'^invoice/$', views.getInvocePdf, name='getInvocePdf'),
    url(r'^getinvoce', views.getInvoce, name='getInvoce'),
    #url(r'^getitemstored$', views.getItemStored, name='getItemStored'),
    url(r'^endoforder/', views.endOfOrder, name='endOfOrder'),
    url(r'^myorders/', views.orderList, name='orderList'),

    url(r'^cart/$', views.cart, name='cart'),
    url(r'^item/(?P<itemSlug>\w+)', views.itemPage, name='item'),
    url(r'^itemlist/$', views.itemList, name='itemlist'),
    url(r'^itemlist/(?P<cls>\w+)', views.itemListSelection, name='itemlistselection'),
    url(r'^login/$',  RedirectView.as_view(pattern_name='account/login')),
    #url(r'^logout', views.logoutUser, name='logoutUser'),
    url(r'^order/$', views.makeOrder, name='order')
    #url(r'^registration', views.registerUser, name='registerUser'),
    #url(r'^setcart', views.setCart, name='setCart')
]
