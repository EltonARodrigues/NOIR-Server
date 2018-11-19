from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, TemplateView, DetailView, View
from django.shortcuts import redirect, render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse
from django.utils import timezone
from .models import Valores, Cadastro
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .forms import MedicaoForm
from .serializers import ValuesSerializer, ValuesFileSerializer
from django.db.models import Avg, Max, Min, Sum, Count
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.decorators import api_view, list_route
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import viewsets, status
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
import json
import requests
from io import StringIO


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

class Graph(LoginRequiredMixin, TemplateView):
    template_name = 'graficos.html'
    model = Valores

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        lowest_values = []
        higher_values = []
        avg_values = []

        cadastros = Cadastro.objects.filter(author_id = self.request.user)
        if self.kwargs.get('pk') == None:
            context['lists'] = cadastros
            context['selec'] = ''
            return context

        elif Cadastro.objects.filter(id = int(self.kwargs.get('pk')), author_id = self.request.user):

            qs = Valores.objects.filter(id = int(self.kwargs.get('pk')))

            for n in ['temperature', 'humidity', 'co', 'co2', 'mp25']:
                try:
                    lowest_values.append(list(qs.aggregate(Min(n)).values())[0])
                    higher_values.append(list(qs.aggregate(Max(n)).values())[0])
                    avg_values.append(round(list(qs.aggregate(Avg(n)).values())[0],2))
                except:
                    pass

            context['lists'] = cadastros
            context['count'] = Valores.objects.filter(id_id=self.kwargs.get('pk')).count()
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

class ClientViewSetJSON(viewsets.ModelViewSet):
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



class ClientViewSetCSV(viewsets.ModelViewSet):

    queryset = Valores.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    serializer_class = ValuesFileSerializer
    #authentication_classes = [BaseAuthentication]
    #permission_classes = (IsAuthenticated, )

    def get_renderer_context(self):
        context = super(ClientViewSetCSV, self).get_renderer_context()
        context['header'] = (
            self.request.GET['fields'].split(',')
            if 'fields' in self.request.GET else None)
        return context

    @list_route(methods=['POST'])
    def csv_upload(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_303_SEE_OTHER)

#### old ###

def nova_medicao(request):
    if request.method == "POST":
        form = MedicaoForm(request.POST)
        if form.is_valid():

            medicao = form.save(commit=False)
            medicao.author = request.user
            medicao.published_date = timezone.now()

            medicao.save()
            if request.FILES:
                csv_file = request.FILES["file_csv"]
                file_data = csv_file.read().decode("utf-8")

                #com = Valores()

                f = StringIO(file_data)
                print(file_data)
                #r = requests.post('http://localhost:8000/api/csv/', files={'teste.csv':file_data })

            return redirect('get_context_data', pk=medicao.pk)
    else:
        form = MedicaoForm()
    return render(request, 'setup.html', {'form': form})

'''
@csrf_exempt
def get_values(request):
    global id_pk
    if request.method=='POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        com = Valores()
        com.co = received_json_data['co']
        com.co2 = received_json_data['co2']
        com.pm25 = received_json_data['mp25']
        com.data = '2000-03-03'#received_json_data['created_at']
        com.temperatura = received_json_data['temperature']
        com.umidade = received_json_data['humidity']
        #com.cadastro_id = int(id_pk)
        #com.cadastro = medicao
        com.save()

        return redirect('get_context_data', pk=medicao.pk)
        #return StreamingHttpResponse('it was post request: '+str(received_json_data))
        # '''