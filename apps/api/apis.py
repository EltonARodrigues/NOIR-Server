from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ModelViewSet
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer

from apps.dashboard.models import GasesCollected

from .serializers import ValuesSerializer


class ClientViewSetJSON(ModelViewSet):
    queryset = GasesCollected.objects.all()
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
    queryset = GasesCollected.objects.all()
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
