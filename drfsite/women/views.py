from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
)
from rest_framework import generics
# CreateAPIView – создание данных по POST-запросу;
# ListAPIView – чтение списка данных по GET-запросу;
# RetrieveAPIView – чтение конкретных данных (записи) по GET-запросу;
# DestroyAPIView – удаление данных (записи) по DELETE-запросу;
# UpdateAPIView – изменение записи по PUT- или PATCH-запросу;
# ListCreateAPIView – для чтения (по GET-запросу) и создания списка данных (по POST-запросу);
# RetrieveUpdateAPIView – чтение и изменение отдельной записи (GET-, PUT- и PATCH-запросы);
# RetrieveDestroyAPIView – чтение (GET-запрос) и удаление (DELETE-запрос) отдельной записи;
# RetrieveUpdateDestroyAPIView – чтение, изменение и добавление отдельной записи (GET-, PUT-, PATCH- и DELETE-запросы).
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Women
# from django.forms.models import model_to_dict
from .serializers import WomenSerializer


def women_index(request: HttpRequest) -> HttpResponse:  # Описываем действия
    # def index_view(request: HttpRequest, pk) -> HttpResponse:  # Описываем действия для Functional view
    # conf_logging(level=logging.DEBUG)
    w_items = Women.objects.all()[:3]
    return render(
        request,
        template_name="women/index.html",
        context={"women": w_items},  # Обращение в БД за всеми элементами
    )
    # return HttpResponse("Страница приложения women.")


class WomenListView(ListView):  # ListView - готовые объекты для отображения из django.views.generic
    model = Women


class WomenDetailView(DetailView):  # делаем свой класс на основе TemplateView. Детальный вид
    model = Women


class WomenListIndexView(ListView):  # делаем свой класс на основе TemplateView. Выводим список
    template_name = "women/index.html"
    queryset = Women.objects.all()


# класс, по которому возвращается список записей в JSON-формате по REST_FRAMEWORK
class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


# класс для отображения содержимого БД или внесения изменений в БД по REST_FRAMEWORK
class WomenAPIView(APIView):  # отображение на основе классов по REST_FRAMEWORK!!!

    def get(self, request):
        w = Women.objects.all()
        return Response({'posts': WomenSerializer(w, many=True).data})

    def post(self, request):
        # serializer = WomenSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )

        return Response({'post': WomenSerializer(post_new).data})
        # return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})
