from .models import *
from rest_framework import serializers
from django.db.models import Sum

class ContestantSerializer(serializers.ModelSerializer):

    contestant_images = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()

    class Meta:
        model = ContestantInfo
        fields ='__all__'
    def get_contestant_images(self,instance):
        images = ContestanInfoImages.objects.filter(contestant = instance)
        serializer = ContestantImageSerializers(images,many=True)
        return serializer.data
    
    def get_votes(self,instance):
        votes = Votes.objects.filter(contestant=instance).aggregate(total_sum=Sum('vote'))['total_sum'] or 0
        return votes
    
class ContestantImageSerializers(serializers.ModelSerializer):
    uploaded_files = serializers.ListField(child=serializers.FileField(),write_only=True,required=False)
    class Meta:
        model = ContestanInfoImages
        fields='__all__'

    def create(self,validated_data):
        uploaded_files = validated_data.pop('uploaded_files',None)
        contestant = validated_data.pop('contestant')

        if uploaded_files:
            for file in uploaded_files:
                ContestanInfoImages.objects.create(contestantdata_images=file,contestant=contestant )

        return contestant
    
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields='__all__'