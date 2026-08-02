from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("restaurants/", include("restaurants.urls")),
    path("menu/", include("menu.urls")),
    path("cart/", include("cart.urls")),
    path("checkout/", include("checkout.urls")),
    path("orders/", include("orders.urls")),
    path("reviews/", include("reviews.urls")),
    path("wishlist/", include("wishlist.urls")),
    path("contact/", include("contact.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("payments/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)