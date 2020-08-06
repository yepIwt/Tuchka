from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse

def index(request):
	return render(request,'main/index.html',{})
