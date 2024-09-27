from django.db import models
from users.models import EVENT
# Create your models here.
import os

class ContestantInfo(models.Model):
    class Meta:
        verbose_name = 'Contestant'
        verbose_name_plural = 'Contestants'
    name = models.CharField(max_length=225)
    event = models.ForeignKey(EVENT,on_delete=models.CASCADE)

    def __str__(self):
        return f'Contestant name : {self.name}, Event title {self.event.name_of_event}'

class ContestanInfoImages(models.Model):
    class Meta:
        verbose_name = 'Contestant Image'
        verbose_name_plural = 'Contestant Images'
    contestant = models.ForeignKey(ContestantInfo,on_delete=models.CASCADE,null=True,blank=True)
    contestantdata_images = models.FileField(upload_to='contestants/',null=True,blank=True)
    prime_image = models.BooleanField(default=False)


    def delete(self,*args, **kwargs):

        if self.contestantdata_images:
            if os.path.isfile(self.contestantdata_images.path):
                os.remove(self.contestantdata_images.path)
        super().delete(*args,**kwargs)


    def __str__(self):
        return f'{self.contestant} image'
    
class Votes(models.Model):
    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural='Votes'
    event = models.ForeignKey(EVENT,on_delete=models.CASCADE)
    contestant = models.ForeignKey(ContestantInfo,on_delete=models.CASCADE)
    vote = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Number of votes is {self.vote} and the total number of votes at this state is {self.event.total_balance}"