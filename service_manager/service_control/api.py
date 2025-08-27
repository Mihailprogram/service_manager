from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ServiceAccess
from .services import SystemService

class BaseAPIView(APIView):
    """Базовый класс для API views"""
    permission_classes = [AllowAny]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_name = 'nginx'
        self.system_service = SystemService(self.service_name)
    
    def get_access(self):
        """Получить объект доступа"""
        access, created = ServiceAccess.objects.get_or_create(
            service_name=self.service_name,
            defaults={'access_allowed': False}
        )
        return access
    
    def check_access(self):
        """Проверить разрешен ли доступ"""
        access = self.get_access()
        return access.access_allowed

class ServiceStatusAPIView(BaseAPIView):
    """API для получения статуса сервиса"""
    
    def get(self, request):
        status_val = self.system_service.get_status()
        access_allowed = self.check_access()
        
        return Response({
            'service': self.service_name,
            'status': status_val,
            'access_allowed': access_allowed
        })

class AccessStatusAPIView(BaseAPIView):
    """API для получения статуса доступа"""
    
    def get(self, request):
        access_allowed = self.check_access()
        
        return Response({
            'service': self.service_name,
            'access_allowed': access_allowed
        })

class AccessControlAPIView(BaseAPIView):
    """API для управления доступом"""
    
    def post(self, request, action):
        access = self.get_access()
        
        if action == 'enable':
            access.access_allowed = True
            message = 'Доступ разрешен'
        elif action == 'disable':
            access.access_allowed = False
            message = 'Доступ запрещен'
        else:
            return Response({
                'status': 'error',
                'message': 'Неверное действие'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        access.save()
        
        return Response({
            'status': 'success',
            'access_allowed': access.access_allowed,
            'message': message
        })

class ServiceControlAPIView(BaseAPIView):
    """API для управления сервисом"""
    
    def post(self, request, action):
        # Проверяем доступ
        if not self.check_access():
            return Response({
                'status': 'error',
                'message': 'Доступ запрещен. Сначала разрешите доступ.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Проверяем допустимость действия
        if action not in ['start', 'stop', 'restart']:
            return Response({
                'status': 'error',
                'message': 'Неверное действие'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Выполняем действие
        success = False
        if action == 'start':
            success = self.system_service.start()
        elif action == 'stop':
            success = self.system_service.stop()
        elif action == 'restart':
            success = self.system_service.restart()
        
        if success:
            new_status = self.system_service.get_status()
            return Response({
                'status': 'success',
                'message': f'Сервис {self.service_name} {action} успешно',
                'current_status': new_status
            })
        else:
            return Response({
                'status': 'error',
                'message': f'Не удалось выполнить {action} для сервиса {self.service_name}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ToggleAccessAPIView(BaseAPIView):
    """API для переключения доступа"""
    
    def post(self, request):
        access = self.get_access()
        access.access_allowed = not access.access_allowed
        access.save()
        
        return Response({
            'status': 'success',
            'access_allowed': access.access_allowed,
            'message': 'Доступ ' + ('разрешен' if access.access_allowed else 'запрещен')
        })