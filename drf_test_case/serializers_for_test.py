from rest_framework import serializers
from .models_for_test import MyModel, PrefixModel # Assuming test_runner.py is in the same dir

class MyModelSerializer(serializers.ModelSerializer):
    prefix_fk = serializers.SerializerMethodField()
    class Meta:
        model = MyModel
        fields = ['id', 'name', 'prefix_fk']
    def get_prefix_fk(self, obj):
        return obj.prefix_fk.name if obj.prefix_fk else None
