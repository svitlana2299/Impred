from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class NetModels(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    description = models.CharField(max_length=150, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modelpath = models.FileField(upload_to='models/', null=False)

    def __str__(self):
        return f"{self.name}"


# class_names = ['Airplane', 'Automobile', 'Bird', 'Cat', 'Deer', 'Dog', 'Frog', 'Horse', 'Ship', 'Truck']
class Labels(models.Model):
    id = models.AutoField(primary_key=True)
    predict_id = models.IntegerField(null=False)
    name = models.CharField(max_length=30, null=False)
    netmodel = models.ForeignKey(NetModels, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ('id', 'predict_id',)

class Images(models.Model):
    name = models.CharField(max_length=30, null=False)
    netmodel = models.ForeignKey(NetModels, on_delete=models.CASCADE, null=True)
    predict = models.ForeignKey(Labels, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    imagepath = models.ImageField(upload_to='images/', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name}"

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.imagepath)

        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img)
            img.save(self.imagepath)
 