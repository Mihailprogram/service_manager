from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .api import (
    ServiceStatusAPIView,
    AccessStatusAPIView,
    AccessControlAPIView,
    ServiceControlAPIView,
    ToggleAccessAPIView
)

# Параметры
service_name_param = openapi.Parameter(
    'service_name', 
    openapi.IN_QUERY, 
    description="Имя сервиса", 
    type=openapi.TYPE_STRING,
    default='nginx'
)

# Декораторы для методов
ServiceStatusAPIView.get = swagger_auto_schema(
    operation_description="Получить статус сервиса",
    operation_summary="Статус сервиса",
    responses={
        200: openapi.Response(
            'Успешный ответ',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'service': openapi.Schema(type=openapi.TYPE_STRING),
                    'status': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_allowed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            )
        )
    }
)(ServiceStatusAPIView.get)

AccessStatusAPIView.get = swagger_auto_schema(
    operation_description="Получить статус доступа",
    operation_summary="Статус доступа",
    responses={
        200: openapi.Response(
            'Успешный ответ',
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'service': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_allowed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                }
            )
        )
    }
)(AccessStatusAPIView.get)

AccessControlAPIView.post = swagger_auto_schema(
    operation_description="Управление доступом (enable/disable)",
    operation_summary="Управление доступом",
    manual_parameters=[
        openapi.Parameter(
            'action', 
            openapi.IN_PATH, 
            description="Действие: enable или disable", 
            type=openapi.TYPE_STRING,
            enum=['enable', 'disable']
        )
    ],
    responses={
        200: openapi.Response('Доступ изменен'),
        400: openapi.Response('Неверное действие'),
    }
)(AccessControlAPIView.post)

ServiceControlAPIView.post = swagger_auto_schema(
    operation_description="Управление сервисом (start/stop/restart)",
    operation_summary="Управление сервисом",
    manual_parameters=[
        openapi.Parameter(
            'action', 
            openapi.IN_PATH, 
            description="Действие: start, stop или restart", 
            type=openapi.TYPE_STRING,
            enum=['start', 'stop', 'restart']
        )
    ],
    responses={
        200: openapi.Response('Успешное выполнение'),
        403: openapi.Response('Доступ запрещен'),
        500: openapi.Response('Ошибка выполнения'),
    }
)(ServiceControlAPIView.post)

ToggleAccessAPIView.post = swagger_auto_schema(
    operation_description="Переключить доступ",
    operation_summary="Переключение доступа",
    responses={
        200: openapi.Response('Доступ переключен'),
    }
)(ToggleAccessAPIView.post)