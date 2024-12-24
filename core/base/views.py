from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from chat.models import TBRooms, TBMessages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from datetime import datetime, timedelta
from django.contrib import messages

class Login(LoginView):
    template_name = 'login/main.html'

    def form_invalid(self, form):
        # Adiciona uma mensagem de erro personalizada
        messages.error(self.request, 'Usuário ou senha inválido. Por favor, tente novamente.')
        # Chama a implementação original do form_invalid, que normalmente retorna para a mesma página de login
        return super().form_invalid(form)

class Index(LoginRequiredMixin, TemplateView):
    template_name = 'index/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['occurrences'] = [
            TBRooms.objects.filter(status = 0).count(),
            TBRooms.objects.filter(status = 1).count(),
            TBRooms.objects.filter(status = 2).count(),
            TBRooms.objects.filter(status = 3).count(),
            TBRooms.objects.filter(status = 4).count()
        ]
        context['total_messages'] = []
        context['date_messages'] = []
        date = datetime.now().date()
        for i in range(5):
            context['total_messages'].append(TBMessages.objects.filter(date__icontains = date).count())
            context['date_messages'].append(str(date))
            date -= timedelta(days = 1)
        context['total_messages'].reverse()
        context['date_messages'].reverse()
        return context

    def post(self, *args, **kwargs):
        room = TBRooms(status = 1)
        room.save()
        return redirect(reverse_lazy('chat', args = [room.pk]))
