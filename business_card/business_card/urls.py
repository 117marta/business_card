from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rae.views import (
    LPMultistepView,
    display_data,
    generate_data,
    index,
    login_view,
    lp_step4,
    register_view,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("generate-data/", generate_data, name="generate-data"),
    path("display-data/", display_data, name="display-data"),
    path("lp-multistep/<str:url>/", LPMultistepView.as_view(), name="lp-multistep"),
    path("lp-step4/", lp_step4, name="lp-step4"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
