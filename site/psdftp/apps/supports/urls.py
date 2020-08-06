from django.urls import path

from . import views

app_name = 'supports'
urlpatterns = [
	path('',views.list,name='list'),
	path('to/',views.support,name='support'),
	path('<str:sname>',views.thanks,name="thanks")
] 
