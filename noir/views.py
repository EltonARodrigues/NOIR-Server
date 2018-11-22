from django.views.generic import CreateView, View, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, Max, Min, Sum, Count
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, reverse
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.viewsets import ModelViewSet
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer
from rest_framework import status, generics
from .serializers import ValuesSerializer
from .models import Valores, Cadastro
from .forms import MeasureForm

from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

from io import StringIO
import requests
import json

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class SelecaoView(View):
    initial = {'key': 'value'}
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('get_context_data')

        return render(request, self.template_name)

class SelecaoView2(View):
    initial = {'key': 'value'}
    template_name = 'teste.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('get_context_data')

        return render(request, self.template_name)


class Graph(LoginRequiredMixin, TemplateView):
    template_name = 'graficos.html'
    model = Valores

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        lowest_values = list()
        higher_values = list()
        avg_values = list()

        cadastros = Cadastro.objects.filter(author_id=self.request.user)
        if self.kwargs.get('pk') is None:
            context['lists'] = cadastros
            context['selec'] = ''
            return context

        elif Cadastro.objects.filter(id=int(self.kwargs.get('pk')),
                                     author_id=self.request.user):

            qs = Valores.objects.filter(id=int(self.kwargs.get('pk')))

            for n in ['temperature', 'humidity', 'co', 'co2', 'mp25']:
                try:
                    lowest_values.append(
                        list(qs.aggregate(Min(n)).values())[0])
                    higher_values.append(
                        list(qs.aggregate(Max(n)).values())[0])
                    avg_values.append(
                        round(list(qs.aggregate(Avg(n)).values())[0], 2))
                except BaseException:
                    pass

            context['lists'] = cadastros
            context['count'] = Valores.objects.filter(
                id_id=self.kwargs.get('pk')).count()
            context['avg_values'] = avg_values
            context['lowest_values'] = lowest_values
            context['higher_values'] = higher_values
            context['temp'] = [q.temperature for q in qs]
            context['hum'] = [q.humidity for q in qs]
            context['co'] = [q.co for q in qs]
            context['co2'] = [q.co2 for q in qs]
            context['pm'] = [q.mp25 for q in qs]
            context['x'] = [q for q in range(len(qs))]

            return context
        else:
            return context


class ClientViewSetJSON(ModelViewSet):
    queryset = Valores.objects.all()
    serializer_class = ValuesSerializer

    def get_renderer_context(self):
        context = super(ClientViewSetJSON, self).get_renderer_context()
        context['header'] = (
            self.request.GET['fields'].split(',')
            if 'fields' in self.request.GET else None)
        return context

    @list_route(methods=['POST'])
    def json_upload(self, request, *args, **kwargs):
        serializer = ValuesSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClientViewSetCSV(ModelViewSet):

    queryset = Valores.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (CSVRenderer,) + \
        tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    serializer_class = ValuesSerializer

    def get_renderer_context(self):
        context = super(ClientViewSetCSV, self).get_renderer_context()
        context['header'] = (
            self.request.GET['fields'].split(',')
            if 'fields' in self.request.GET else None)
        return context

    @list_route(methods=['POST'])
    def csv_upload(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MeasureView(FormView):
    template_name = 'setup.html'
    form_class = MeasureForm
    success_url = '/medicao/'

    def form_valid(self, form):
        medicao = form.save(commit=False)
        medicao.author = self.request.user
        medicao.published_date = timezone.now()

        medicao.save()
        if self.request.FILES:
            csv_file = self.request.FILES["file_csv"]
            file_data = csv_file.read().decode("utf-8")

            f = StringIO(file_data)
            print(file_data)

            ClientViewSetCSV()
        return super().form_valid(medicao)

