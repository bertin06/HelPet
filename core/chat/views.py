from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import TBMessages, TBRooms
from django.shortcuts import redirect
from django.db.models.query import Q
from django.contrib import messages
import emoji

class ChatList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'chat-list/main.html'
    model = TBRooms

    def get_queryset(self):
        queryset = super().get_queryset().order_by('status')
        if not self.request.user.is_staff:
            queryset = queryset.filter(fkusercli = self.request.user)
        elif not self.request.user.is_superuser:
            queryset = queryset.filter(Q(status = 0) | Q(fkuserpro = self.request.user))
        return queryset
    
    def post(self, request, **kwargs):
        action = self.request.POST.get('action')
        if action == 'new-chat':
            room = TBRooms(
                fkusercli = self.request.user,
                status = 0
            )
            room.save()
            return redirect(reverse_lazy('chat', args = [room.pk]))
        if action == 'open-chat':
            room = TBRooms.objects.get(pk = self.request.POST.get('room'))
            if self.request.user.is_staff and room.status == 0:
                room.fkuserpro = self.request.user
                room.status = 1
                room.save()
                return redirect(reverse_lazy('chat', args = [room.pk]))
            elif self.request.user == room.fkuserpro or self.request.user == room.fkusercli:
                return redirect(reverse_lazy('chat', args = [room.pk]))
            else:
                messages.error(request, 'Ocorrência já em execução')
                return redirect(reverse_lazy('chat-list'))

class Chat(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'chat/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tbroom'] = TBRooms.objects.get(pk = kwargs.get('room'))
        context['tbmessages'] = TBMessages.objects.filter(fkroom__pk = kwargs.get('room'))
        context['emojis'] = list(emoji.EMOJI_DATA.keys())
        return context
    
    def post(self, request, **kwargs):
        TBRooms.objects.filter(pk = kwargs.get('room')).update(status = self.request.POST.get('conclusion'))
        messages.success(request, 'Ocorrência finalizada')
        return redirect(reverse_lazy('chat-list'))
