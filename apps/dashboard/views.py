from io import StringIO

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Max, Min
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView, TemplateView, View

from apps.api.viewsets import GasesCollectedViewSet

from .forms import MeasureForm
from .models import GasesCollected, Sensor

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
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        lowest_values = list()
        higher_values = list()
        avg_values = list()

        cadastros = Sensor.objects.filter(author_id=self.request.user)
        if self.kwargs.get('pk') is None:
            context['lists'] = cadastros
            context['selec'] = ''
            return context

        elif Sensor.objects.filter(id=self.kwargs.get('pk'),
                                   author_id=self.request.user):

            qs = GasesCollected.objects.filter(
                sensor=self.kwargs.get('pk')
            ).order_by('-created_at')[:100]

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
            context['count'] = qs.count()
            context['avg_values'] = avg_values
            context['lowest_values'] = lowest_values
            context['higher_values'] = higher_values
            context['temp'] = [q.temperature for q in qs]
            context['hum'] = [q.humidity for q in qs]
            context['co'] = [q.co for q in qs]
            context['co2'] = [q.co2 for q in qs]
            context['pm'] = [q.mp25 for q in qs]
            context['x'] = [q for q in range(qs.count())]

            return context
        else:
            return context


class MeasureView(FormView):
    template_name = 'measuring_form.html'
    form_class = MeasureForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        medicao = form.save(commit=False)
        medicao.author = self.request.user
        medicao.published_date = timezone.now()

        medicao.save()
        if self.request.FILES:
            csv_file = self.request.FILES["file_csv"]
            file_data = csv_file.read().decode("utf-8")

            StringIO(file_data)
            print(file_data)

            GasesCollectedViewSet()
        return super().form_valid(medicao)
