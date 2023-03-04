from django.shortcuts import render
from django.views.generic import (
    TemplateView, 
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from django.urls import reverse_lazy
# models
from .models import Empleado
# forms
from .forms import EmpleadoForm

# Create your views here.

class InicioView(TemplateView):
    """Vista que carga la pagina de incio"""
    template_name = 'inicio.html'

class ListAllEmpleados(ListView):
    template_name = 'persona/list_all.html'
    paginate_by = 4
    ordering = 'first_name'
    context_object_name = 'empleados'

    def get_queryset(self):
        palabra_clave = self.request.GET.get('kword', '')
        lista = Empleado.objects.filter(
            first_name__icontains= palabra_clave
        )
        return lista


class ListaEmpleadosAdmin(ListView):
    template_name = 'persona/lista_empleados.html'
    paginate_by = 10
    ordering = 'first_name'
    context_object_name = 'empleados'
    model = Empleado


class ListByAreaEmpleado(ListView):
    """lista de empleados de un area"""
    template_name = 'persona/list_area.html'
    context_object_name = 'empleados'
    
    def get_queryset(self):
        #aqui el codigo que yo quiera, pero siempre debe retornar una lista de elementos
        area = self.kwargs['shorname']
        lista = Empleado.objects.filter(
            departamento__shor_name= area
        )
        return lista

class ListEmpleadosByKword(ListView):
    """ lista empleados por palabra clave """
    template_name = 'persona/by_kword.html'
    context_object_name = 'empleados'
    
    def get_queryset(self):
        print('************')
        palabra_clave = self.request.GET.get('kword', '')
        lista = Empleado.objects.filter(
            first_name = palabra_clave
        )
        return lista
    
class ListHabilidadesEmpleado(ListView):
    template_name = 'persona/habilidades.html'
    context_object_name = 'habilidades'
    
    def get_queryset(self):
        id_clave = self.request.GET.get('id',)
        empleado = Empleado.objects.get(
             id = id_clave
        )
        return empleado.habilidades.all()
    

class EmpleadoDetailView(DetailView):
    model = Empleado
    template_name = "persona/detail_empleado.html"
    
    def get_context_data(self, **kwargs):
        context = super(EmpleadoDetailView, self).get_context_data(**kwargs)
        context['titulo'] = 'Empleado del mes'
        return context
    

class SuccessView(TemplateView):
    template_name = "persona/success.html"



class EmpleadoCreateView(CreateView):
    template_name = "persona/add.html"
    model = Empleado
    #fields = ['first_name', 'last_name' , 'job']
    form_class = EmpleadoForm
    success_url = reverse_lazy('persona_app:empleados_admin')
    
    def form_valid(self, form):
        #logica del proceso
        empleado = form.save(commit=False)
        empleado.full_name = empleado.first_name + ' ' + empleado.last_name
        empleado.save()
        return super(EmpleadoCreateView, self).form_valid(form)
    
    
class EmpleadoUpdateView(UpdateView):
    template_name = "persona/update.html"
    model = Empleado
    fields = [
         'first_name',
         'last_name',
         'job',
         'departamento',
         'habilidades'
    ]
    
    success_url = reverse_lazy('persona_app:empleados_admin')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print('*********METODO POST**********')
        print('===================')
        print(request.POST)
        print(request.POST['last_name'])
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        #logica del proceso
        print('*********METODO FORM VALID**********')
        print('*******************')
        return super(EmpleadoUpdateView, self).form_valid(form)
    

class EmpleadoDeleteView(DeleteView):
    template_name = "persona/delete.html"
    model = Empleado
    success_url = reverse_lazy('persona_app:empleados_admin')
