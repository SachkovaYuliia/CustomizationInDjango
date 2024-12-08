# 7. (REST API та DRF) Налаштуйте ендпоінт із фільтрацією даних та кастомними дозволами.
# Реалізуйте серіалізатор із вкладеними полями.from rest_framework import serializers

from .models import CustomModel, Category
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CustomModelSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = CustomModel
        fields = ['id', 'title', 'content', 'category', 'created_at']
