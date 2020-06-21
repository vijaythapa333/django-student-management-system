from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from student_management_system import settings
from student_management_app import views


urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
