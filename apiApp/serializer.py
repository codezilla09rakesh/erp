from rest_framework import serializers
from account.models import CustomUser, MyProfile
from holiday.models import Leave, YourEmployee, Resions
from django.shortcuts import redirect


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     # \help_text='Leave empty if no change needed',
    style={'input_type': 'password', 'placeholder': 'Password'})
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_manager']

    def create(self, validated_data):
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=225)
    password = serializers.CharField(style={'input_type': 'password'})

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyProfile
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        # fields = ['title', 'description', 'starting_date', 'ending_date', 'half_day', 'status']
        fields = "__all__"
    # def create(self, validated_data):
    #     leave = super(LeaveSerializer, self).create(validated_data)
    #     user = self.context['request'].user
    #     user = CustomUser.objects.get(username=user)
    #     manager = YourEmployee.objects.get(employee = user)
    #     leave.employee = user
    #     leave.manager = manager
    #     leave.save()
    #     return leave
    def validate(self, data):
        ending_date = data.get('ending_date', None)
        half_day = data.get('half_day', None)
        if half_day is None:
            half_day = "select"
        half_day = half_day.strip(" ").lower()
        print('ending_data', ending_date)
        print('half_day', half_day)
        if ending_date:
            print('in side of end date')
        else:
            print('out sido of end')
        if half_day=="first_half" or half_day=="second_half":
            if ending_date:
                print('in side of half day')
                raise serializers.ValidationError("You can select only either an end date or days ")
        else:
            if half_day == "select" and ending_date==None:
                print('select any one')
                raise serializers.ValidationError("Please Select Any One Ending Date or Half Day")
        return data

class YourEmployeeSerializer(serializers.ModelSerializer):
    # manager = serializers.StringRelatedField()
    # employee = serializers.StringRelatedField()
    class Meta:
        model = YourEmployee
        fields = "__all__"

class ResionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resions
        fields = "__all__"

class AcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"


class LoginAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", "password")
        extra_kwargs = {
            "username": {
                "required": True,
                "error_messages": {"required": "Please fill username field", },
            },
            "password": {
                "required": True,
                "error_messages": {"required": "Please fill password field", },
            },
        }