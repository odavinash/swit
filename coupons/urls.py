"""coupons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.contrib.admin.sites import AdminSite
from rest_framework_swagger.views import get_swagger_view
from django.conf import settings


schema_view = get_swagger_view(title='Datingapp API')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view),
    path('coupon/', include('discount_coupons.urls', namespace='coupon')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


AdminSite.site_header = 'Coupons Admin Panel'
AdminSite.site_title = 'Coupons'
AdminSite.index_title = ''
