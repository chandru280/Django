from django.db import models

 

class Sample(models.Model):
    name = models.CharField(max_length=10)
    standard = models.CharField(max_length=10)
    marks = models.PositiveIntegerField()

    def __str__(self):
        return self.name
class Qrcode(models.Model):
    name = models.ForeignKey(Sample, on_delete=models.CASCADE)
    code = models.ImageField(blank=True, upload_to='code')

     