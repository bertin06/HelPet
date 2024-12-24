from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q

class UserList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'user/main.html'
    model = User

    def post(self, request, **kwargs):
        action = self.request.POST.get('action')
        if self._valid_user() == True:
            if action == 'new-user':
                self._new_user()
                messages.success(request, 'Usuário criado')
            if action == 'edit-user':
                self._edit_user()
                messages.success(request, 'Usuário atualizado')
        else:
            messages.error(request, 'Usuário já cadastrado')
        return redirect(reverse_lazy('user-list'))
    
    def _new_user(self):
        user = User(
            username = self.request.POST.get('username'),
            first_name = self.request.POST.get('first_name'),
            last_name = self.request.POST.get('last_name'),
            is_superuser = True if self.request.POST.get('type') == '1' else False,
            is_staff = True if self.request.POST.get('type') != '2' else False
        )
        user.set_password(self.request.POST.get('password'))
        user.save()

    def _edit_user(self):
        user = User.objects.get(pk = self.request.POST.get('user'))
        user.username = self.request.POST.get('username')
        user.first_name = self.request.POST.get('first_name')
        user.last_name = self.request.POST.get('last_name')
        user.is_superuser = True if self.request.POST.get('type') == '1' else False
        user.is_staff = True if self.request.POST.get('type') != '2' else False
        user.save()
    
    def _valid_user(self):
        try:
            User.objects.get(Q(username = self.request.POST.get('username')), ~Q(pk = self.request.POST.get('user')))
            return False
        except:
            return True

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect(reverse_lazy('login'))