import subprocess

class SystemService:
    def __init__(self, service_name='nginx'):
        self.service_name = service_name
    
    def get_status(self):
        """Получить статус сервиса"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', self.service_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout.strip()
        except:
            return 'unknown'
    
    def start(self):
        """Запустить сервис"""
        return self._execute_command('start')
    
    def stop(self):
        """Остановить сервис"""
        return self._execute_command('stop')
    
    def restart(self):
        """Перезапустить сервис"""
        return self._execute_command('restart')
    
    def _execute_command(self, action):
        """Выполнить команду управления сервисом"""
        try:
            if action == 'start':
                subprocess.run(['sudo', 'systemctl', 'start', self.service_name], timeout=10)
            elif action == 'stop':
                subprocess.run(['sudo', 'systemctl', 'stop', self.service_name], timeout=10)
            elif action == 'restart':
                subprocess.run(['sudo', 'systemctl', 'restart', self.service_name], timeout=10)
            return True
        except:
            return False