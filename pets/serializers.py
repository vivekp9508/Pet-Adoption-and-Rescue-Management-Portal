from rest_framework import serializers
from .models import PetReport, Notification

class PetReportSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = PetReport
        fields = '__all__'
        read_only_fields = ['user', 'status', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

class PetReportStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetReport
        fields = ['status', 'admin_note']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'