from rest_framework.serializers import ModelSerializer
from .models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "category_type",
        )
        # exclude = ("created_at",)
