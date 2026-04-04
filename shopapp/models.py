from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.
units = {"Lt": "Litro", 
         "Kg": "Kilogramo", 
         "Pza": "Pieza", 
         "Caja": "Caja", 
         "Paquete": "Paquete", 
         "Rollos": "Rollos"
}

class Division(models.Model):
    name = models.CharField(max_length=50, verbose_name="Division")

    class Meta:
        verbose_name = 'Division'
        verbose_name_plural = 'Divisions'

    def __str__(self) :
        return self.name


#  A family belonges to a division (wal mart example)
class Family(models.Model):
    name = models.CharField(max_length=50, verbose_name="Family")
    division = models.ForeignKey(Division, models.PROTECT, default = 3)
    

    class Meta:
        verbose_name = 'Family'
        verbose_name_plural = 'Families'
    
    def __str__(self) :
        return self.name
    
class Seller(models.Model):
    name = models.CharField(max_length=30, verbose_name="Tienda")
    photo = models.ImageField(upload_to="images/", null=True, blank=True)

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'

    def __str__(self) :
        return self.name

class Article(models.Model):
    name = models.CharField(max_length=60, verbose_name="Descripcion")
    quantity = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=True, verbose_name="Contenido")
    unit = models.CharField(max_length=7,blank=False, verbose_name="Unidad", choices=units.items())
    package = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)], verbose_name="Paquete")
    ean = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999999)], verbose_name="EAN", 
    null=True, blank=True)
    family = models.ForeignKey(Family, models.PROTECT)  
    photo = models.ImageField(upload_to="images/", null=True, blank=True)
    
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self) :
        return self.name
    
class Purchase(models.Model) :
    date = models.DateField(default=timezone.now)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(9999)], verbose_name="Cantidad")
    article = models.ForeignKey(Article, models.PROTECT)
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Precio U")
    note =  models.CharField(max_length=25, blank=True, verbose_name="Comentario")
    seller = models.ForeignKey(Seller, models.PROTECT)

    def price_per_unit_with_unit(self):
        if self.article.quantity > 0:
            price_per_unit = self.price / (self.article.quantity * self.article.package)
            return f"{price_per_unit:.2f} {self.article.unit}"
        return f"0.00 {self.article.unit}"
    
    class Meta:
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'

