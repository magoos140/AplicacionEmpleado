from django.db import models
from aplications.departamento.models import Departamento
from ckeditor.fields import RichTextField

class Habilidades(models.Model):
    habilidad = models.CharField('Habilidad', max_length=50)
    
    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades empleado'
        
    def __str__(self):
        return str(self.id) + '_' + self.habilidad

# Create your models here.
class Empleado(models.Model):
    """ Modelo para tabla empleado """
    JOB_CHOICES = (
        ('0','CONTADOR'),
        ('1','ADMINISTRADOR'),
        ('2','ECONOMISTA'),
        ('3','OTRO'),
    )
    
    
    first_name = models.CharField('Primer Nombre', max_length=60)
    last_name = models.CharField('apellidos', max_length=60)
    avatar = models.ImageField(upload_to="personas", null=True, blank = True)
    full_name = models.CharField(
        'Nombres completos',
        max_length=120,
        blank=True
    )
    job = models.CharField('trabajo', max_length=1, choices=JOB_CHOICES)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    habilidades = models.ManyToManyField(Habilidades)
    hoja_vida = RichTextField(blank=True, null=True)
    
    
    class Meta:
        verbose_name = 'Mi Empleado'
        verbose_name_plural = 'Empleados de la empresa'
        ordering = ['first_name']
        unique_together = ('first_name', 'last_name')
    
    
    def __str__(self):
        return str(self.id) + '_' + self.first_name + '_' + self.last_name