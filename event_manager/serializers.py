from rest_framework import serializers
from django.contrib.auth.models import User
from event_manager.models import EventDb, EventMemberDb

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EventSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = EventDb
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

class EventMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only= True)
    member_username = serializers.CharField(source= 'user.username', read_only = True)
    member_user_id = serializers.IntegerField(source= 'user.id', read_only = True)

    class Meta:
        model = EventMemberDb
        fields = ['id', 'username', 'member_username', 'member_user_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_username(self, value):
        try:
            u = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("This user is not registered")

        e = self.context['event']

        if u == e.created_by:
            raise serializers.ValidationError("Owner cant be added as a member")

        if EventMemberDb.objects.filter(event=e, user=u).exists():
            raise serializers.ValidationError("This user is already a member")

        return value

    def create(self, validated_data):
        username = validated_data.pop("username")
        u = User.objects.get(username=username)
        e = self.context['event']
        return EventMemberDb.objects.create(event=e, user=u)