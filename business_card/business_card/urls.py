from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from rae.views import display_data, generate_data, index, login_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('generate-data/', generate_data, name='generate-data'),
    path('display-data/', display_data, name='display-data'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
