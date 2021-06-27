from django.db import models
from django.db.models import Manager
from django.db.models.signals import m2m_changed, pre_save, post_save
from django.utils.text import slugify
# User = settings.AUTH_USER_MODEL
from django.conf import settings
from .utils import unique_order_id_generator
from django.db.models import signals


class Category(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category


class Attribute(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    atribute = models.CharField(unique=True, max_length=20)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.atribute)
        super(Attribute, self).save(*args, **kwargs)

    def __str__(self):
        return self.atribute


class Configure(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    configure = models.CharField(max_length=50)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True, )
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.configure)
        super(Configure, self).save(*args, **kwargs)

    def __str__(self):
        return self.configure


class Product(models.Model):
    objects = None
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=255, db_index=True, default='')
    price = models.IntegerField(blank=True, null=True)
    main_image = models.ImageField(upload_to='media/products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    attribute = models.ForeignKey(Attribute, on_delete=models.SET_NULL, null=True, blank=True)
    configure = models.ForeignKey(Configure, on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    # @property
    # def name(self):
    #     return self.name


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class Cart(models.Model):
    # objects = None
    objects = CartManager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        print(action)
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()
        print(total)


m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = instance.subtotal + 10    #10 rs for delivery charges
    else:
        instance.total = 0.00


pre_save.connect(pre_save_cart_receiver, sender=Cart)


class Order(models.Model):
    object = None
    ORDER_STATUS_CHOICE = (
        ('created', 'created'),
        ('paid','paid'),
        ('shipped', 'shipped'),
        ('refunded', 'refunded'),
    )
    order_id = models.CharField(max_length=120, blank=True)
    # billing_profile =
    # shipping_address =
    # billing_address =
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,)
    status = models.CharField(max_length=120, default='created', choices= ORDER_STATUS_CHOICE)
    shipping_total = models.DecimalField(default=10, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return str(self.order_id)

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = cart_total + shipping_total
        self.total = new_total
        self.save()
        return new_total


def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)


pre_save.connect(pre_save_create_order_id, sender=Order)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.object.filter(cart_id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()


post_save.connect(post_save_cart_total, sender=Cart)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    print("running")
    if created:
        print("updating")
        instance.update_total()


post_save.connect(post_save_cart_total, sender=Order)