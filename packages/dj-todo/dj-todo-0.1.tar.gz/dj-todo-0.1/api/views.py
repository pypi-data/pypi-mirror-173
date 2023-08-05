from functools import partial
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.decorators import api_view, APIView
from rest_framework import generics, mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
import datetime
from django.db.models import Q


# Create your views here.


def home(request):
    return HttpResponse('Welcome to my Task App')


@api_view(['GET'])
def tasks_statistics(request):
    try:
        queryset = Task.objects.filter(
            created_by=request.user)
        data = {
            "due": queryset.filter(status="Due").count(),
            "todo": queryset.filter(status="New").count(),
            "done": queryset.filter(status="Success").count()
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Error in fetching counts", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_due_task(request):
    try:
        print(datetime.datetime.now())
        queryset = Task.objects.filter(
            due_date__lt=datetime.datetime.now(), status="New")
        due_tasks = queryset.count()
        queryset.update(status="Due")
        queryset = Task.objects.filter(
            due_date__gt=datetime.datetime.now(), status="Due")
        due_tasks = queryset.count()
        queryset.update(status="New")
        data = {
            "due_tasks": due_tasks,
        }
        return Response(data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"message": "Error in fetching counts", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TaskList(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = request.GET.get('query')
        if query:
            queryset = Task.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query), created_by=request.user).order_by('status')
        else:
            queryset = Task.objects.filter(
                created_by=request.user).order_by('status')
        serialized = TaskSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        serialized = TaskSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save(created_by=request.user)
            tags = request.data.get("tag_ids", None)
            if tags:
                tag_objs = []
                for tag in tags:
                    tag_obj = TagTaskMapping(
                        tag_id=tag, task_id=serialized.data.get('id'))
                    tag_objs.append(tag_obj)
                TagTaskMapping.objects.bulk_create(tag_objs)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        task_obj = get_object_or_404(Task, pk=pk)
        serialized = TaskSerializer(task_obj, data=request.data, partial=True)
        if serialized.is_valid():
            serialized.save(created_by=request.user)
            tags = request.data.get("tag_ids", None)
            existing_tags = list(TagTaskMapping.objects.filter(
                task_id=serialized.data.get('id')).values_list("tag_id", flat=True))
            print('Incoming tags', tags)
            print('Existing tags', existing_tags)
            adding_tags = list(set(tags)-set(existing_tags))
            removing_tags = list(set(existing_tags)-set(tags))
            print("adding_tags", adding_tags, "removing_tags", removing_tags)
            if tags:
                tag_objs = []
                for tag in adding_tags:
                    tag_obj = TagTaskMapping(
                        tag_id=tag, task_id=serialized.data.get('id'))
                    tag_objs.append(tag_obj)
                TagTaskMapping.objects.bulk_create(tag_objs)
                TagTaskMapping.objects.filter(
                    tag_id__in=removing_tags).delete()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)


class TagList(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        query = request.GET.get('query')
        if query:
            queryset = Tag.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query), created_by=request.user).order_by('status')
        else:
            queryset = Tag.objects.filter(
                created_by=request.user).order_by('status')
        serialized = TagSerializer(queryset, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        serialized = TagSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save(created_by=request.user)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serialized.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = Appuser.objects.all()
    serializer_class = ApppuserSerializer
    permission_classes = [AllowAny]
