from rest_framework import serializers
from account.models import CustomUser

class Register(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_manager')

    def create(self, validated_data):
        pass
