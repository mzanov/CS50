from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_store/", views.add_store, name="add_store"),
    path('extract_info/', views.extract_info, name='extract_info'),
    path("scan_receipts", views.scan_receipts, name="scan_receipts"),
    path("create_reward", views.create_reward, name="create_reward"),
    path("reward_list", views.reward_list, name="reward_list"),
    path("redeem_reward/<int:reward_id>", views.redeem_reward, name="redeem_reward"),
    path('generate_image_identifier/', views.generate_image_identifier, name='generate_image_identifier')
]