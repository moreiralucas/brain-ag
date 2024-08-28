from django.db import models


class RuralProducer(models.Model):
    document = models.CharField("CPF or CNPJ", max_length=14)
    producer_name = models.CharField(max_length=128)
    farm_name = models.CharField(max_length=128)
    city  = models.CharField(max_length=32)
    state = models.CharField(max_length=32)
    total_area = models.DecimalField(max_digits=10, decimal_places=2)
    agricultural_area = models.DecimalField(max_digits=10, decimal_places=2)
    vegetation_area = models.DecimalField(max_digits=10, decimal_places=2)

class Crops(models.Model):
    name = models.CharField(max_length=128)
    producer = models.ForeignKey("core.RuralProducer", on_delete=models.CASCADE, related_name="crops")
