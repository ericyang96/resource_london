from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from calculator import views as calculator_views

urlpatterns = [
	#defining url for form
	url(r'^calculator/', calculator_views.calculatorform),
	path('accounts/', include('django.contrib.auth.urls')),
	url(r'^register/$', calculator_views.register, name='register'),
    url(r'^admin/', admin.site.urls),
	path('', RedirectView.as_view(url='accounts/login/')),
	url(r'download/', calculator_views.download_data, name='download_data')
]
