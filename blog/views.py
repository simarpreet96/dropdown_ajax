from urllib import request

from django.http import Http404
from django.views.generic import DetailView

from .models import Product, Category, Configure, Attribute, Cart, CartManager, Order
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
            return redirect('index')
    else:
        form = ProductForm()
    allproducts = Product.objects.filter()
    allsubcategory = Category.objects.filter()
    allattribute = Attribute.objects.filter()
    allconfigure = Configure.objects.filter()
    return render(request, 'product.html', locals())


def product_detail(request, slug):
    product= get_object_or_404(Product, slug=slug)
    return render(request,'product_detail.html', locals())

# def load_cities(request):
#     country_id = request.GET.get('country')
#     cities = City.objects.filter(country_id=country_id).order_by('name')
#     return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def load_cities(request):
    # attribute_id = request.GET.get('id_attribute')   #attribute_id_list
    attribute_id = request.GET['attribute']
    print(attribute_id, '2222222')
    configures = Configure.objects.filter(attribute_id=attribute_id).order_by('slug')
    print(configures, "7777777777777")
    return render(request, 'city_dropdown_list_options.html', {'configures': configures})


# def cart_create(user=None):
#     cart_obj = Cart.objects.create(user=None)
#     print("new cart created")
#     return (cart_obj)


# class ProductDetailSlugView(DetailView):
#     queryset = Product.objects.all()
#     template_name = "product_detail.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
#         cart_obj, new_obj = Cart.objects.new_or_get(self.request)
#         context['cart'] = cart_obj
#         return context
#
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get('slug')
#     try:
#         instance = Product.objects.get(slug=slug, active=True)
#     except Product.DoesNotExist:
#         raise Http404("Not Found")
#     except Product.MultipleObjectsReturend:
#         qs = Product.objects.filter(slug=slug, active=True)
#         instance = qs.first()
#     except:
#         raise Http404("ummmm")
#     return instance


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # print(request.session, '@@@@')
    # key=request.session.session_key
    # print(key, '$$$$')
    # print(request.session.get('username', 'unknown'))
    return render(request, 'cart.html', locals())


# def cart_update(request):
#     print(request.POST)
#     product_id = request.POST.get('product_id')
#     if product_id is None:
#         try:
#             product_obj = Product.objects.get(id=product_id)
#         except Product.DoesNotExist:
#             print("Show message to user product is gone")
#             return redirect('index')
#         cart_obj, new_obj = Cart.objects.new_or_get(request)
#         if product_obj in cart_obj.products.all():
#             cart_obj.products.remove(product_obj)   # use to remove m2m products field
#         else:
#             cart_obj.products.add(product_obj)  # cart_obj.products.add(product_id)   # use to add m2m products field
#     # return redirect(product_obj.get_absolute_url())
#     return redirect('index')


def cart_update(request):
    print(request.POST)
    product_id = request.POST.get('product_id')
    product_obj = Product.objects.get(id=product_id)
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)   # use to remove m2m products field
    else:
        cart_obj.products.add(product_obj)  # use to add m2m products field
    request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())
    return redirect('cart_home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if not cart_created or cart_obj.count() == 0:
        return redirect('index')
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    return render(request, "checkout.html", locals())