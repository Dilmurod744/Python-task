from django.db.models import Model, CharField, TextField, ImageField, IntegerField, DecimalField, DateTimeField, \
    BooleanField, \
    ForeignKey, CASCADE, SlugField, ManyToManyField
from django.utils.text import slugify
from mptt.models import MPTTModel


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(Model):
    title = CharField(max_length=25)
    slug = SlugField(max_length=25, null=True, blank=True, unique=True)
    parent = ManyToManyField("self", symmetrical=False, blank=True, related_name="children", )

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)


class Shop(BaseModel):
    title = CharField(max_length=255)
    description = TextField()
    image = ImageField(upload_to='shop_images')
    slug = SlugField(max_length=25, null=True, blank=True, unique=True)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)


class Product(BaseModel):
    description = TextField(max_length=2550)
    title = CharField(max_length=255)
    amount = IntegerField(default=1)
    price = DecimalField(max_digits=9, decimal_places=2)
    active = BooleanField(default=False)
    slug = SlugField(max_length=25, null=True, blank=True, unique=True)
    shop = ForeignKey('apps.Shop', on_delete=CASCADE, related_name='shops')
    category = ManyToManyField('apps.Category', related_name='product_category', blank=True)

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.title)
        return super().save(force_insert, force_update, using, update_fields)


class ProductImage(BaseModel):
    image = ImageField(upload_to='product_images')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='product_images')
