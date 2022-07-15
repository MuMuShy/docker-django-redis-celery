from urllib import response
from .models import Task
from .serializers import TaskSerializer
from django.http import Http404
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from linebot import (
    WebhookParser,WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
handler = WebhookHandler('a99e4ca4fcc2fb56aba9baf978b13126') 
class BaseCallbackView(View):
    line_channel_class = None
    event_handler_class = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # assert self.line_channel_class
        #assert self.event_handler_class

        headers = request.headers
        signature = headers['X-Line-Signature']

        body = request.body.decode()

        # line_channel = self.line_channel_class()
        # line_channel.secret = 'a99e4ca4fcc2fb56aba9baf978b13126'

        parser = WebhookParser('a99e4ca4fcc2fb56aba9baf978b13126')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponse('Bad Request', 400)

        # handler = self.event_handler_class(request)
        for event in events:
            handler.handle_event(event)

        return HttpResponse('ok')

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskDetail(APIView):
    
    def get_object(self, task_id):
        try:
            return Task.objects.get(pk = task_id)
        except Task.DoesNotExist:
            raise Http404
    
    def get(self, request, task_id, formate = None):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    def put(self, request, task_id, formate=None):
        task = self.get_object(task_id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id, format = None):
        task = self.get_object(task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
