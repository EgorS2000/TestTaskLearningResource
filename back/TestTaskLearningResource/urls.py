from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = (
    path('admin/', admin.site.urls),
    path('LearningRosource-auth/', include('rest_framework.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('api.homework_api.urls')),
    path('api/', include('api.info_api.urls')),
    path('api/', include('api.quiz_api.urls')),
    path('api/', include('api.test_api.urls'))
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
