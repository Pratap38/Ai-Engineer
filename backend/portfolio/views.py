from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from pathlib import Path
from urllib.parse import urlencode
from .models import Conversation, Message
from .ai.hr_assistant import HRAssistant

PROFILE_PATH = Path(__file__).resolve().parent.parent.parent / "Ai-Engineer" / "AiPortfolio" / "profile.json"

_PROFILE_CACHE = None

def load_profile():
    """Read profile.json once and keep it in memory."""
    global _PROFILE_CACHE
    if _PROFILE_CACHE is None:
        if PROFILE_PATH.exists():
            with open(PROFILE_PATH) as f:
                _PROFILE_CACHE = json.load(f)
        else:
            _PROFILE_CACHE = {}
    return _PROFILE_CACHE

SUGGESTIONS = [
    "Give me his resume",
    "What projects has he built?",
    "Tell me about his work at Roomhy",
    "What are his hobbies?",
]

def chat_view(request):
    return render(request, 'portfolio/chat.html', {
        'profile': load_profile(),
        'conversations': Conversation.objects.all()[:30],
        'suggestions': SUGGESTIONS,
    })

def conversation_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    return render(request, 'portfolio/conversation.html', {
        'conversation': conversation,
        'messages': conversation.messages.all(),
        'profile': load_profile(),
        'conversations': Conversation.objects.all()[:30],
    })

def new_conversation(request):
    """Create a conversation then redirect, so a refresh doesn't spawn another."""
    conversation = Conversation.objects.create()
    url = reverse('conversation', args=[conversation.id])
    q = request.GET.get('q', '').strip()
    if q:
        url += '?' + urlencode({'q': q})
    return redirect(url)

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)

    user_message = (data.get('message') or '').strip()
    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)

    # Read history BEFORE saving the new message, otherwise the message gets
    # sent to the model twice (once from history, once as the new turn).
    history = [
        {'role': m.role, 'content': m.content}
        for m in conversation.messages.all()
    ]

    Message.objects.create(conversation=conversation, role='hr', content=user_message)

    try:
        ai_response = HRAssistant().chat(user_message, history)
    except Exception as e:
        # Surface the real reason (rate limit, bad key, ...) instead of a 500 page.
        return JsonResponse({'error': f'{type(e).__name__}: {e}'}, status=502)

    Message.objects.create(conversation=conversation, role='assistant', content=ai_response)
    conversation.save(update_fields=['updated_at'])

    return JsonResponse({'success': True, 'response': ai_response})
