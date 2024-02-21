from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.

class PublicBlog(APIView):
    def get(self,request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            page_number = request.GET.get('page',1)
            paginator = Paginator(blogs, 3)
            serializer = BlogSerializer(paginator.page(page_number), many = True)

            return Response(
                    {
                     'data': serializer.data,
                     'message':'Blogs Fetched Successfully'
                    }
                    ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                    {
                     'data': {},
                     'message':'something went wrong or invalid page number'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)



class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            blogs = Blog.objects.filter(user = request.user)

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))

            serializer = BlogSerializer(blogs, many = True)
            return Response(
                    {
                     'data': serializer.data,
                     'message':'Blogs Fetched Successfully'
                    }
                    ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                    {
                     'data': {},
                     'message':'something went wrong'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)
            
            if not serializer.is_valid():
                return Response(
                    {
                     'data': serializer.errors,
                     'message':'something went wrong'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(
                    {
                     'data': serializer.data,
                     'message':'Blog created successfully'
                    }
                    ,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                    {
                     'data': {},
                     'message':'something went wrong'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uuid = data.get('uuid'))

            if not blog.exists():
                return Response(
                    {
                     'data': {},
                     'message':'Invalid blog id'    
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response(
                    {
                     'data': {},
                     'message':'You are not authorized to update'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
            
            serializer = BlogSerializer(blog[0], data=data, partial = True)

            if not serializer.is_valid():
                return Response(
                    {
                     'data': serializer.errors,
                     'message':'something went wrong'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(
                    {
                     'data': serializer.data,
                     'message':'Blog updated successfully'
                    }
                    ,status=status.HTTP_200_OK)
            

        except Exception as e:
            return Response(
                    {
                     'data': {},
                     'message':'something went wrong'
                    }
                    ,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        data = request.data
        blog = Blog.objects.filter(uuid = data.get('uuid'))

        if not blog.exists():
            return Response(
                {
                 'data': {},
                 'message':'Invalid blog id'    
                }
                ,status=status.HTTP_400_BAD_REQUEST)
        if request.user != blog[0].user:
            return Response(
                {
                 'data': {},
                 'message':'You are not authorized to delete'
                }
                ,status=status.HTTP_400_BAD_REQUEST)
        
        blog[0].delete()
        return Response(
                   {
                    'data': {},
                    'message':'Blog deleted successfully'
                   }
                   ,status=status.HTTP_200_OK)