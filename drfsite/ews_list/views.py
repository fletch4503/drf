from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from django.views.generic import CreateView, ListView, DetailView, FormView, View
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
# from rest_framework.response import Response
# from rest_framework.views import APIView
from .models import ewsitem
from .forms import ewsitemForm
# from django.forms.models import model_to_dict
from .serializers import ewsitemSerializer
from .exch_lib_model import pwp_exch_model


# Здесь определяем Functional Based View - отображение на основе функций!!!
def index_view(request: HttpRequest) -> HttpResponse:  # Описываем действия
    # def index_view(request: HttpRequest, pk) -> HttpResponse:  # Описываем действия для Functional view
    # conf_logging(level=logging.DEBUG)
    ews_items = ewsitem.objects.all()[:3]  # свойство objects есть в БД сортировкой по id. Выводим 3 элемента
    # ews_items = ewsitem.objects.get(pk=pk)  # действия для Functional view -> если не нашли - делаем, исключение
    # ews_items = ewsitem.objects.order_by("id").all()  # свойство objects есть в БД сортировкой по id
    data = {'title': 'EWS List Приложение!!!'}
    return render(
        request,
        template_name="ews_list/index.html",
        context={"ews_items": ews_items},  # Обращение в БД за всеми элементами
    )


# Вид на основе классов - класс создания элемента
class ewsitemCreateView(CreateView):
    model = ewsitem
    form_class = ewsitemForm
    template_name = "ews_list/ewsitem_form.html"
    # def get_success_url(self):
    #     # success_url = super().get_success_url()
    #     #     obj = self.object
    #     #     print(f'получили success_url: {success_url}, для объекта: {str(obj)}')
    #     #     additional_param = 'example_param'
    #     return reverse(
    #         "ews_list:detail",
    #         kwargs={"pk": self.object.pk},
    #     )
    # return "{0}?param={1}".format(success_url, additional_param)


class ewsitemFormView(FormView):  # создаем вид на основе формы ewsitemForm из Form
    # specify the Form you want to use
    form_class = ewsitemForm
    fields = '__all__'
    # specify name of template
    template_name = "ews_list/ewsitem_add.html"
    success_url = '/'
    # success_url = reverse_lazy('/')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    # can specify success url
    # url to redirect after successfully
    # updating details


class ewsitemView(View):

    def get(self):
        ews_items = ewsitem.objects.all()[:3]
        return HttpResponse(
            template_name="ews_list/ewsitem_detail.html",
            context={"ews_items": ews_items},  # Обращение в БД за всеми элементами
        )


class ewsitemList(ListView):
    model = ewsitem
    template_name = "ews_list/ewsitem_list.html"
    mpe = pwp_exch_model()  # Объект для подключения к почте Exchange
    total_count = 0
    for i in range(0, len(mpe.msg_cnt_list)):
        total_count = total_count + mpe.msg_cnt_list[i]
    if total_count == 0:
        print("ewsitemList - У вас нет входящих сообщений")
    else:
        print(f'ewsitemList - У вас {total_count} входящих сообщений')


class ewsitemListIndexView(ListView):
    model = ewsitem
    template_name = "ews_list/index.html"
    queryset = ewsitem.objects.all()[:3]


class ewsitemDetailView(DetailView):
    model = ewsitem

    # override context data
    def get_context_data(self, **kwargs):
        context = super(ewsitemDetailView,
                        self).get_context_data(**kwargs)
        # add extra field
        context["category"] = "cat_id"
        return context


# класс, по которому возвращается список записей в JSON-формате
class ewsAPIList(generics.ListCreateAPIView):
    queryset = ewsitem.objects.all()
    serializer_class = ewsitemSerializer


# класс для отображения содержимого БД или внесения изменений в БД REST_FRAMEWORK
# class ewsAPIView(APIView):  # - отображение на основе классов!!!
#
#     def get(self, request):
#
#         w = ewsitem.objects.all()
#         return Response({'posts': ewsitemSerializer(w, many=True).data})
#
#     def post(self, request):
#         serializer = ewsitemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # post_new = Women.objects.create(
#         #     title=request.data['title'],
#         #     content=request.data['content'],
#         #     cat_id=request.data['cat_id']
#         # )
#
#         # return Response({'post': WomenSerializer(post_new).data})
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = ewsitem.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = ewsitemSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({"post": serializer.data})


def about(request):
    return render(
        request,
        template_name="about.html",
    )
