"""
Фоновый воркер для обработки задач
"""
import time
import sqlite3
import requests
from datetime import datetime, timedelta

def check_devices():
    """Проверка онлайн статуса устройств"""
    while True:
        try:
            conn = sqlite3.connect('stelzon_logs.db')
            c = conn.cursor()
            
            # Отмечаем устройства offline если нет активности 5 минут
            c.execute('''UPDATE devices 
                         SET status = 'offline' 
                         WHERE datetime(last_seen) < datetime('now', '-5 minutes')''')
            
            conn.commit()
            conn.close()
        except:
            pass
        
        time.sleep(60)  # Проверка каждую минуту

if __name__ == "__main__":
    check_devices()
