from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
	
def index(request):
    return render(request, template_name='index.html')

@require_POST
@csrf_exempt
def example(request):
	print('This is the webhook request.', request.POST.items())
	return HttpResponse('This is the webhook response.')
