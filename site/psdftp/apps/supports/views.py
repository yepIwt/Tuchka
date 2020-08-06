from django.shortcuts import render
from django.utils import timezone
from .models import Support
from django.http import Http404,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

def list(request):
	sup = Support.objects.order_by('-date')
	return render(request,'supports/list.html',{'supports': sup})

def support(request):
	sup = Support(name = request.POST['name'], date = timezone.now())
	sup.save()
	return HttpResponseRedirect(reverse('supports:thanks',args=(sup.name,)))

def thanks(request,sname):
	try:
		sup = Support.objects.filter(name__startswith = sname)[0]
	except:
		raise Http404("You're not a support >:")

	return render(request,'supports/thanks.html',{'support':sup})