from django.urls import path
from .views import BlogApiView


urlpatterns = [
    path('get-blogs', BlogApiView.as_view(), name='blogs'),
    path('delete-blog/<int:blog_id>', BlogApiView.as_view(), name='delete_blog'),
    path('create-blog', BlogApiView.as_view(), name='create_blog'),
    path('update-blog/<int:blog_id>', BlogApiView.as_view(), name='update_blog')
]