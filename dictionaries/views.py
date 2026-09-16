from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404 
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Dictionary, DictionaryVersion, DictionaryElement
from .serializers import RefbookSerializer, RefbookElementSerializer



class RefbookListView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='date',
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Дата начала действия в формате ГГГГ-ММ-ДД.'
            )
        ]
    )
    def get(self, request):
        date_param = request.query_params.get('date')
        queryset = Dictionary.objects.all()

        if date_param:
            try:
                parsed_date = datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(versions__start_date__lte=parsed_date).distinct()
            except ValueError:
                return Response(
                    {"error": "Неверный формат даты. Используйте ГГГГ-ММ-ДД"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = RefbookSerializer(queryset, many=True)
        return Response({"refbooks": serializer.data})



class RefbookElementsView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='version',
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Версия справочника. Если не указана, возвращаются элементы текущей версии.'
            )
        ]
    )
    def get(self, request, pk):
        dictionary = get_object_or_404(Dictionary, pk=pk)
        version_param = request.query_params.get('version')

        if version_param:
            version_obj = DictionaryVersion.objects.filter(
                dictionary=dictionary, 
                version=version_param
            ).first()
        else:
            today = timezone.now().date()
            version_obj = DictionaryVersion.objects.filter(
                dictionary=dictionary,
                start_date__lte=today
            ).order_by('-start_date').first()

        if not version_obj:
            return Response({"elements": []})

        elements = DictionaryElement.objects.filter(version=version_obj)
        serializer = RefbookElementSerializer(elements, many=True)
        return Response({"elements": serializer.data})



class RefbookCheckElementView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='id',
                type=int,
                location=OpenApiParameter.PATH,
                description='Идентификатор справочника',
                required=True
            ),
            OpenApiParameter(
                name='code',
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Код элемента справочника'
            ),
            OpenApiParameter(
                name='value',
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Значение элемента справочника'
            ),
            OpenApiParameter(
                name='version',
                type=str,
                location=OpenApiParameter.QUERY,
                required=False,
                description='Версия справочника. Если не указана, проверяется текущая версия.'
            )
        ]
    )

    def get(self, request, pk):
        dictionary = get_object_or_404(Dictionary, pk=pk)
        
        code = request.query_params.get('code')
        value = request.query_params.get('value')
        version_param = request.query_params.get('version')

        if not code or not value:
            return Response(
                {"error": "Параметры 'code' и 'value' обязательны для заполнения."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if version_param:
            version_obj = DictionaryVersion.objects.filter(
                dictionary=dictionary, 
                version=version_param
            ).first()
        else:
            today = timezone.now().date()
            version_obj = DictionaryVersion.objects.filter(
                dictionary=dictionary,
                start_date__lte=today
            ).order_by('-start_date').first()

        if not version_obj:
            return Response({"valid": False, "message": "Действующая версия справочника не найдена."})

        exists = DictionaryElement.objects.filter(
            version=version_obj,
            code=code,
            value=value
        ).exists()

        if exists:
            return Response({"valid": True})
        else:
            return Response({"valid": False, "message": "Элемент с такими данными в указанной версии отсутствует."})
        