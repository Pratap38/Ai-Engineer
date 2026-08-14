from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('conversation/<uuid:conversation_id>/', views.conversation_view, name='conversation'),
    path('conversation/<uuid:conversation_id>/send/', views.send_message, name='send_message'),
    path('conversation/new/', views.new_conversation, name='new_conversation'),
]
