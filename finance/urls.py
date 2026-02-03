from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),

    # OpenAPI / Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Auth (JWT + register + me + pages)
    path("api/auth/", include("accounts.urls")),

    # Transactions CRUD
    path("api/", include("transactions.urls")),

    # Reports (summary)
    path("api/", include("reports.urls")),

    # Dashboard page
    path("dashboard/", TemplateView.as_view(template_name="dashboard/index.html"), name="dashboard"),
    
    path("api/", include("transactions.urls")),

]
