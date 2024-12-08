from django.forms.widgets import Select

class CustomSelectWidget(Select):
    template_name = 'widgets/custom_select.html'

    def __init__(self, attrs=None, choices=()):
        attrs = attrs or {'class': 'custom-select'}
        super().__init__(attrs, choices)