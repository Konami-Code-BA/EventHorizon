from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.views.decorators.http import require_POST
	
def index(request):
    return render(request, template_name='index.html')

@require_POST
def example(request):
	print('This is the webhook request.', request)
	return HttpResponse('This is the webhook response.')
