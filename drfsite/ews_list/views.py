# from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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
from .models import ewsitem
# from django.forms.models import model_to_dict
from .serializers import ewsitemSerializer


# Здесь определяем Functional Based View - отображение на основе функций!!!
def index_view(request: HttpRequest) -> HttpResponse:  # Описываем действия
    # def index_view(request: HttpRequest, pk) -> HttpResponse:  # Описываем действия для Functional view
    # conf_logging(level=logging.DEBUG)
    ews_items = ewsitem.objects.all()[:3]  # свойство objects есть в БД сортировкой по id. Выводим 3 элемента
    # ews_items = ewsitem.objects.get(pk=pk)  # действия для Functional view -> если не нашли - делаем, исключение
    # ews_items = ewsitem.objects.order_by("id").all()  # свойство objects есть в БД сортировкой по id

    return render(
        request,
        template_name="ews_list/index.html",
        context={"ews_items": ews_items},  # Обращение в БД за всеми элементами
    )


# класс, по которому возвращается список записей в JSON-формате
class ewsAPIList(generics.ListCreateAPIView):
    queryset = ewsitem.objects.all()
    serializer_class = ewsitemSerializer


# класс для отображения содержимого БД или внесения изменений в БД REST_FRAMEWORK
class ewsAPIView(APIView):  # - отображение на основе классов!!!

    def get(self, request):

        w = ewsitem.objects.all()
        return Response({'posts': ewsitemSerializer(w, many=True).data})

    def post(self, request):
        serializer = ewsitemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # post_new = Women.objects.create(
        #     title=request.data['title'],
        #     content=request.data['content'],
        #     cat_id=request.data['cat_id']
        # )

        # return Response({'post': WomenSerializer(post_new).data})
        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = ewsitem.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer = ewsitemSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})
