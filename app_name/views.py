from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.views.decorators.http import require_POST

@require_POST
def example(request):
	print(request)
	return HttpResponse('This is the webhook response.')