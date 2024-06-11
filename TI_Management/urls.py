from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from TI_Management_app.views import Image, ImageDisplay


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),
    # path('', include('TI_Management_app.urls')),
    path('', include('TI_Management_app.urls', namespace='TI_Management_app')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    # path('images/', Image.as_view(), name='image'),
    # path('images/<int:pk>/', ImageDisplay.as_view(), name="image_display"),
]

handler404 = 'TI_Management_app.views.error_404_view'
# handler500 = 'TI_Management_app.views.error_500_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

