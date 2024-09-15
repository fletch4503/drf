# from django.shortcuts import render
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


# класс, по которому возвращается список записей в JSON-формате
class ewsAPIList(generics. ListCreateAPIView):
    queryset = ewsitem.objects.all()
    serializer_class = ewsitemSerializer

# класс для отображения содержимого БД или внесения изменений в БД
class ewsAPIView(APIView):

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

