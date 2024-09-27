from typing import Any, Dict
from users.models import *
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVENT
        fields='__all__'
        
class REFRESHSERIALIZER(TokenRefreshSerializer):
    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        return super().validate(attrs)
    
class TOKENSERIALIZER(TokenObtainPairSerializer):
    def validate(self,attrs):
        data = super().validate(attrs)
        data['name']=self.user.name
        data['email']=self.user.email
        data['phone']=self.user.phone
        data['organization']=self.user.organization
        data['id']=self.user.id

        return data
    
class USERMODELSERIALIZER(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_active = serializers.CharField(write_only=True)
    is_staff = serializers.CharField(write_only=True)
    is_admin = serializers.CharField(write_only=True)
    is_superuser = serializers.CharField(write_only=True)
    createAt = serializers.CharField(write_only=True)
    updatedAt = serializers.CharField(write_only=True)
    groups = serializers.CharField(write_only=True)
    user_permissions = serializers.CharField(write_only=True)
    
    class Meta:
        model = USERMODEL
        fields='__all__'