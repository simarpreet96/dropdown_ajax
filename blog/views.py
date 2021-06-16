from django.shortcuts import render
from .models import Product, Category, Configure, Attribute
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm


def index(request):
    return render(request, 'index.html')


def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            print("11111111111")
            product = form.save(commit=False)
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    allproducts = Product.objects.filter()
    allsubcategory = Category.objects.filter()
    allattribute = Attribute.objects.filter()
    allconfigure = Configure.objects.filter()
    print("333333333333" ,allproducts)
    return render(request, 'index.html', locals())



# def load_cities(request):
#     country_id = request.GET.get('country')
#     cities = City.objects.filter(country_id=country_id).order_by('name')
#     return render(request, 'city_dropdown_list_options.html', {'cities': cities})

def load_cities(request):
    attribute_id = request.GET.get('attribute')   #attribute_id_list
    print(attribute_id, '2222222')
    configures = Configure.objects.filter(attribute_id=attribute_id).order_by('slug')
    print(configures , "7777777777777")
    return render(request, 'city_dropdown_list_options.html', {'configures': configures})