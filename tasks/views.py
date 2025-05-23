# tasks/views.py
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Count, Q, Case, When, Value, CharField
from django.utils import timezone

from .models import Task, Category, Notification # Import Notification
from .forms import TaskForm, CategoryForm

# --- Existing Task Views ---
class HomeView(TemplateView):
    template_name = 'home.html'

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        status = self.request.GET.get('status')
        category_id = self.request.GET.get('category')
        search_query = self.request.GET.get('q')
        due_date_filter = self.request.GET.get('due_date_filter')

        if status == 'completed':
            queryset = queryset.filter(completed=True)
        elif status == 'pending':
            queryset = queryset.filter(completed=False)

        if category_id:
            try:
                category = Category.objects.get(pk=category_id, user=self.request.user)
                queryset = queryset.filter(category=category)
            except Category.DoesNotExist:
                pass

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(description__icontains=search_query)
            )

        if due_date_filter:
            now = timezone.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

            if due_date_filter == 'overdue':
                queryset = queryset.filter(completed=False, due_date__lt=now)
            elif due_date_filter == 'today':
                queryset = queryset.filter(due_date__range=(today_start, today_end))
            elif due_date_filter == 'this_week':
                end_of_week = today_end + timezone.timedelta(days=6)
                queryset = queryset.filter(due_date__range=(now, end_of_week))
            elif due_date_filter == 'later':
                end_of_week = today_end + timezone.timedelta(days=6)
                queryset = queryset.filter(due_date__gt=end_of_week)
            elif due_date_filter == 'no_due_date':
                queryset = queryset.filter(due_date__isnull=True)


        queryset = queryset.order_by('completed', 'due_date', '-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user=self.request.user).order_by('name')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_search_query'] = self.request.GET.get('q', '')
        context['current_due_date_filter'] = self.request.GET.get('due_date_filter', '')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

# --- Category Views ---
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'tasks/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        current_user = self.request.user
        user_categories_queryset = Category.objects.filter(user=current_user)
        annotated_categories = user_categories_queryset.annotate(
            task_count=Count('category_tasks', filter=Q(category_tasks__user=current_user))
        ).order_by('name')
        return annotated_categories

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = 'tasks/category_confirm_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')

    def test_func(self):
        category = self.get_object()
        return category.user == self.request.user

# --- Dashboard View ---
class DashboardView(LoginRequiredMixin, View):
    template_name = 'tasks/dashboard.html'

    def get(self, request, *args, **kwargs):
        user_tasks = Task.objects.filter(user=request.user)
        now = timezone.now()
        one_week_from_now = now + timezone.timedelta(days=7)

        total_tasks = user_tasks.count()
        completed_tasks = user_tasks.filter(completed=True).count()
        pending_tasks = user_tasks.filter(completed=False).count()

        overdue_tasks_list = user_tasks.filter(
            completed=False,
            due_date__lt=now
        ).order_by('due_date')

        tasks_due_soon_list = user_tasks.filter(
            completed=False,
            due_date__range=(now, one_week_from_now)
        ).exclude(pk__in=overdue_tasks_list.values_list('pk', flat=True)).order_by('due_date')

        overdue_tasks_count = overdue_tasks_list.count()
        tasks_due_soon_count = tasks_due_soon_list.count()

        tasks_by_category_detailed = user_tasks.annotate(
            category_name=Case(
                When(category__isnull=False, then='category__name'),
                default=Value('No Category'),
                output_field=CharField()
            )
        ).values('category_name').annotate(
            count=Count('category_name')
        ).order_by('category_name')

        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks_count': overdue_tasks_count,
            'tasks_due_soon_count': tasks_due_soon_count,
            'overdue_tasks_list': overdue_tasks_list,
            'tasks_due_soon_list': tasks_due_soon_list,
            'tasks_by_category': tasks_by_category_detailed,
            'username': request.user.username,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        if task_id:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            if request.POST.get('action') == 'mark_complete':
                task.completed = True
                task.save()
            elif request.POST.get('action') == 'mark_pending':
                task.completed = False
                task.save()
        return redirect('dashboard')

# NEW VIEW: NotificationListView
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'tasks/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 10 # Optional: paginate notifications

    def get_queryset(self):
        # Fetch all notifications for the current user, ordered by most recent
        queryset = Notification.objects.filter(user=self.request.user).order_by('-created_at')
        # Mark all displayed notifications as read when the page is loaded
        queryset.update(is_read=True) # This will update them in the DB
        return queryset
