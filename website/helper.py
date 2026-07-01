from django.shortcuts import render
from django.shortcuts import HttpResponse
import datetime
def renderhelper(request,folder,htmlpage,context={}):
    return render(request,'website/'+folder+'/'+htmlpage+'.html',context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

