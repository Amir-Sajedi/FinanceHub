from django.db import models

class Price(models.Model):
    code = models.SlugField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    currency = models.CharField(max_length=10, default="IRR")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["code"]
        
    def __str__(self):
        return f"{self.code}: {self.price} {self.currency}"