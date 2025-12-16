#!/usr/bin/env bash
# build.sh для Render.com

echo "🚀 Начинаем сборку StelZon Panel..."

# Устанавливаем зависимости
pip install -r requirements.txt

# Создаем необходимые директории
mkdir -p static/css static/js static/images
mkdir -p templates logs data

echo "✅ Сборка завершена"
