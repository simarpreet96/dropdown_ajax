from django import forms
from .models import Product, Category, Configure, Attribute


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'main_image', 'category', 'attribute', 'configure')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['configure'].queryset = Configure.objects.none()

        if 'attribute' in self.data:
            try:
                attribute_id = int(self.data.get('attribute'))
                self.fields['configure'].queryset = Configure.objects.filter(attribute__id=attribute_id).order_by(
                    'slug')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['configure'].queryset = self.instance.attribute.configure_set.order_by('slug')

