from django.urls import path

from . import views

app_name = 'storage'
urlpatterns = [
	path('',views.index,name='index'),
	#path('dwn/',views.indexdwn, name='indexdwn')
] 
