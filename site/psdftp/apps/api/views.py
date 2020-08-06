from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	return HttpResponse('This is API')

def check(request,method_name):
	return HttpResponse('This is API.' + method_name)