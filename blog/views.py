from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify
from blog.models import Blog


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Контроллер создания статьи"""
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_add_blog'
    extra_context = {'title': 'Создание статьи'}

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, ListView):
    """Контроллер просмотра статей"""
    model = Blog
    template_name = 'blog/blog_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        blog = Blog.objects.all()

        context_data['object_list'] = blog
        context_data['title'] = 'Блог'

        return context_data


class BlogDetailView(LoginRequiredMixin, DetailView):
    """Контроллер просмотра статьи"""
    model = Blog
    template_name = 'blog/blog_detail.html'
    extra_context = {'title': 'Просмотр статьи'}

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Контроллер редактирования статьи"""
    model = Blog
    fields = ('title', 'content', 'preview', 'is_published')
    permission_required = 'blog.can_change_blog'
    extra_context = {'title': 'Редактирование статьи'}

    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Контроллер удаления статьи"""
    model = Blog
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.can_delete_blog'
    extra_context = {'title': 'Удаление статьи'}


def toggle_activity(request, pk):
    """Функция переключения активности статьи"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True

    blog_item.save()
    return redirect(reverse('blog:list'))


def CreateBlogList(request):
    blog_list = Blog.objects.all()
    context = {
        'object_list': blog_list,

    }

    return render(request, 'blog/toggle.html', context)
