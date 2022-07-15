
from django.contrib import admin
from django.urls import path

from core import views as todoapi_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('callback/', todoapi_views.BaseCallbackView.as_view()),
    path('api/task/', todoapi_views.TaskList.as_view(), name='task-list'),
    path('api/task/<int:task_id>/', todoapi_views.TaskDetail.as_view(), name='task-detail'),
]
