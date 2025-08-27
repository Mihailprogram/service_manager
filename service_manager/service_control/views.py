from django.shortcuts import render
from .services import SystemService
from .models import ServiceAccess

def index(request):
    """Главная страница с веб-интерфейсом"""
    service_name = 'nginx'
    system_service = SystemService(service_name)
    status = system_service.get_status()
    
    # Получаем или создаем запись о доступе
    access, created = ServiceAccess.objects.get_or_create(
        service_name=service_name,
        defaults={'access_allowed': False}
    )
    
    return render(request, 'service_control/index.html', {
        'service_name': service_name,
        'status': status,
        'access_allowed': access.access_allowed
    })