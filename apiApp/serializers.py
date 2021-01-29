from rest_framework import serializers
from account.models import CustomUser

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = "__all__"
        exclude = ['password']




