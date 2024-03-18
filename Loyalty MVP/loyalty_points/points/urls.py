from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_store/", views.add_store, name="add_store"),
    path("scan_receipts", views.scan_receipts, name="scan_receipts")
]