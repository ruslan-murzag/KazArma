from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('grocery.urls')),
    path('account/', include('account.urls')),
    path('report/', include('report.urls'))

]
