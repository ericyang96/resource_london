from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

#importing views from newsletter app
from calculator import views as calculator_views

urlpatterns = [
	#defining url for form
	url(r'^calculator/', calculator_views.calculatorform),
	path('accounts/', include('django.contrib.auth.urls')),
	url(r'^register/$', calculator_views.register, name='register'),
    url(r'^admin/', admin.site.urls),
	url(r'download/', calculator_views.download_data, name='download_data')
]
