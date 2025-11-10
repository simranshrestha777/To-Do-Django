from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Task
from django.urls import reverse_lazy
from django.shortcuts import render


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"   # file we'll create
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        # return tasks for the current user, newest first
        return Task.objects.filter(user=self.request.user).order_by("-created_at")

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'completed']  # fields the user can fill
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy('task-list')  # redirect after successful create

    def form_valid(self, form):
        form.instance.user = self.request.user  # set current user
        return super().form_valid(form)
    
class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    template_name = "tasks/task_form.html"  # reuse the form template
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        # Only allow editing tasks of the logged-in user
        return self.model.objects.filter(user=self.request.user)
    
class TaskDeleteView(DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        # Only allow deleting tasks of the logged-in user
        return self.model.objects.filter(user=self.request.user)
    
