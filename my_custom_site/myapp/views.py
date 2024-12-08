from django.shortcuts import render,redirect
from .forms import CustomSelectForm, CustomUserRegistrationForm
from django.views import View
from django.http import JsonResponse
from .models import CustomModel
from django.contrib import messages
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, generics
from .serializers import CustomModelSerializer
from .permissions import IsAdminUser
from django.http import JsonResponse
from .middleware import RequestCountMiddleware
from django.http import HttpResponse
import logging



def custom_form_view(request):
    if request.method == "POST":
        form = CustomSelectForm(request.POST)
        if form.is_valid():
            selected_option = form.cleaned_data['option']
            return render(request, 'myapp/widgets/success.html', {'option': selected_option})
    else:
        form = CustomSelectForm()

    return render(request, 'myapp/widgets/form_for_widget.html', {'form': form})


def success_view(request):
    return render(request, 'success.html', {'message': ' The form successfully sent.'})

def processor_view(request):
    return render(request, 'myapp/context_processor.html')

class CustomModelListView(View):
    """
    CBV для відображення списку елементів CustomModel.
    """
    def get(self, request):
        items = CustomModel.objects.values('id', 'title', 'content', 'created_at')
        return JsonResponse({'items': list(items)})

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully!")
            return redirect('custom_select')
        else:
            print(form.errors)
            messages.error(request, "There was an error with your registration.")
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'myapp/registration/register.html', {'form': form})

class CustomModelListView(generics.ListAPIView):
    queryset = CustomModel.objects.all()
    serializer_class = CustomModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'title']
    search_fields = ['title', 'content']

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

def request_count_view(request):
    count = RequestCountMiddleware.request_count
    return JsonResponse({'request_count': count})

logger = logging.getLogger('myapp')

def test_view(request):
    logger.info("This is test logger info")
    return HttpResponse('Check your logs!')