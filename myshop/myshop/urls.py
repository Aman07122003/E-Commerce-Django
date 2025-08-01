from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('cart/', include("cart.urls", namespace="cart")),
    path('orders/', include("orders.urls", namespace="orders")),
    path('payment/', include("payment.urls", namespace="payment")),
    path('', include("shop.urls", namespace="shop")),



    path("__reload__/", include("django_browser_reload.urls")),  # For live reloading
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
