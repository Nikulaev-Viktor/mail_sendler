from django.urls import path
from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView, toggle_activity, \
    CreateBlogList
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('blog_list/', BlogListView.as_view(), name='list'),
    path('detail/<int:pk>/', BlogDetailView.as_view(),  name='detail'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activity, name='toggle_activity'),
    path('toggle_activity', CreateBlogList, name='toggle')

]
