from django.urls import path
from . import views



urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("supplier/listings/", views.supplier_listings, name="supplier_listings"),
    path("supplier/listings/create/", views.create_listing, name="create_listing"),
    path("supplier/requests/", views.supplier_requests, name="supplier_requests"),
    path("supplier/requests/<int:request_id>/<str:action>/", views.update_request_status, name="update_request_status"),

    path("buyer/listings/", views.buyer_listings, name="buyer_listings"),
    path("buyer/listings/<int:listing_id>/request/", views.create_request, name="create_request"),
    path("buyer/requests/", views.buyer_requests, name="buyer_requests"),
    path("supplier/listings/<int:listing_id>/edit/", views.edit_listing, name="edit_listing"),
    path("supplier/listings/<int:listing_id>/delete/", views.delete_listing, name="delete_listing"),
    path("supplier/requests/<int:request_id>/pay/", views.mark_paid_view, name="mark_paid_supplier"),


    

]
