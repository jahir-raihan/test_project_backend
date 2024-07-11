# Imports

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import Blog
from django.db.models import Q
from .serializer import BlogSerializer


# End Imports

class BlogApiView(APIView):

    """
    API endpoint for getting blogs
    """

    def get(self, request):

        """
        Get serialized blogs including filtration process
        """

        # Get filtering params
        query = request.GET.get('query', '')
        is_active = request.GET.get('is_active', 'all')

        # If the request is from blog edit page then execute this section.
        is_single = request.GET.get('is_single_blog', 'false')

        if is_single == 'true':

            blog_id = request.GET.get('blog_id')
            blog = Blog.objects.get(pk=blog_id)
            serialized_blog = BlogSerializer(blog)

            return Response(serialized_blog.data, status=status.HTTP_200_OK)

        # Prepare filtering q object
        q = Q(blog_title__icontains=query) | Q(blog_body__icontains=query) | Q(author__icontains=query)
        if is_active != 'all':
            is_active = is_active == 'true'
            q &= Q(is_active=is_active)

        # Filter the data
        data = Blog.objects.filter(q).order_by('-created_at')

        # Serialized the data for response
        serialized_data = BlogSerializer(data, many=True)

        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def post(self, request, blog_id=None):

        """
        Create or Update a blog
        """

        data = request.POST

        blog = Blog()
        if blog_id:
            blog = Blog.objects.get(pk=blog_id)

        blog.blog_title = data.get('blog_title')
        blog.author = data.get('author')
        blog.blog_body = data.get('blog_body')
        blog.is_active = data.get('is_active') == 'true'

        blog.save()

        return Response({"message": "Successfully added/updated blog!"}, status=status.HTTP_201_CREATED)

    def delete(self, request, blog_id):

        """
        Delete an blog
        """

        try:
            Blog.objects.get(pk=blog_id).delete()
        except Exception:
            pass

        return Response({"message": "Delete blog successfully!", 'status': 200}, status=status.HTTP_200_OK)