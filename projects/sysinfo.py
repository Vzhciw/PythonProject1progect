import platform
import psutil
from datetime import datetime

def get_size(bytes, suffix="B"):
    """Конвертер байтов в читаемый формат (КБ, МБ, ГБ)"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

print("="*40, "Информация о системе", "="*40)
uname = platform.uname()
print(f"Операционная система: {uname.system} {uname.release}")
print(f"Имя компьютера: {uname.node}")
print(f"Процессор: {uname.processor}")

print("\="*40, "Информация о памяти", "="*40)
svmem = psutil.virtual_memory()
print(f"Всего RAM: {get_size(svmem.total)}")
print(f"Доступно: {get_size(svmem.available)}")
print(f"Использовано: {svmem.percent}%")

print("="*40, "Информация о диске", "="*40)
partition = psutil.disk_usage('/')
print(f"Всего на диске C: {get_size(partition.total)}")
print(f"Свободно: {get_size(partition.free)}")
print(f"Использовано: {partition.percent}%")

print("="*40, "Сеть", "="*40)
net_io = psutil.net_io_counters()
print(f"Отправлено данных: {get_size(net_io.bytes_sent)}")
print(f"Получено данных: {get_size(net_io.bytes_recv)}")