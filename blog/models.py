from django.db import models
from django.utils.text import slugify


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
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, null=True, blank=True,)
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
