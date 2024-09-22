from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class GeneralCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    show_navbar = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        verbose_name = "Ana Kategori"
        verbose_name_plural = "Ana Kategoriler"

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey(GeneralCategory, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = "Alt Kategori"
        verbose_name_plural = "Alt Kategoriler"

    def __str__(self):
        return f"{self.name}"

class BottleType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Materyal"
        verbose_name_plural = "Şişe Materyalleri"

    def __str__(self):
        return self.name

class BottleVolume(models.Model):
    volume = models.PositiveIntegerField(unique=True)

    class Meta:
        ordering = ['volume']
        verbose_name = "Hacim"
        verbose_name_plural = "Şişe Hacimleri"

    def __str__(self):
        return f"{self.volume} mL"


class BottleColor(models.Model):
    name = models.CharField(max_length=100, unique=True, default='Şeffaf')

    class Meta:
        ordering = ['name']
        verbose_name = "Renk"
        verbose_name_plural = "Şişe Renkleri"

    def __str__(self):
        return self.name

class BottleCapType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Ağız Şekli"
        verbose_name_plural = "Ağız Şekilleri"

    def __str__(self):
        return self.name


class Product(models.Model): 
    name = models.CharField(max_length=300, null=False, blank=False)
    short_description = models.CharField(max_length=300, null=True, blank=True)
    long_description = CKEditor5Field('Uzun Açıklama', config_name='extends')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = CKEditor5Field('Notlar', config_name='extends',default='')
    
    general_category = models.ManyToManyField(GeneralCategory)
    sub_category = models.ManyToManyField(SubCategory, blank=True)
    
    product_code = models.CharField(max_length=30, null=False, blank=False)
    bottle_volume = models.ForeignKey(BottleVolume,null=True, blank=True, on_delete=models.PROTECT) #hacim
    bottle_type = models.ForeignKey(BottleType,null=True, blank=True, on_delete=models.PROTECT) #materyal
    bottle_color = models.ForeignKey(BottleColor,null=True, blank=True, on_delete=models.PROTECT) #renk
    bottle_cap_type = models.ForeignKey(BottleCapType,null=True, blank=True, on_delete=models.PROTECT) #agizsekli

    height = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Yükseklik')
    width = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Genişlik')
    diameter = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Çap')
    depth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='En')
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Ağırlık')
    

    best_seller = models.BooleanField(default=False, verbose_name='Çok Satanlar')
    newest = models.BooleanField(default=False, verbose_name='En Yeniler')

    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.short_description)
        super().save(*args, **kwargs)

    def first_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image
        return None

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"


class ProductImage(models.Model):
    IMAGE_TYPE_CHOICES = (
        ('url', 'Görsel Linki'),
        ('upload', 'Yükle'),
    )

    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_type = models.CharField(max_length=10, choices=IMAGE_TYPE_CHOICES, default='upload', verbose_name='Görsel Tipi')
    image_upload = models.ImageField(upload_to='core/img/', blank=True, null=True,verbose_name='Görsel Yükle')
    image_url = models.CharField(max_length=500, blank=True,verbose_name='Görsel Adresi')

    @property
    def image(self):
        if self.image_type == 'upload':
            return self.image_upload.url if self.image_upload else None
        elif self.image_type == 'url':
            return self.image_url
        return None
    
    class Meta:
        verbose_name = "Ürün Fotoğrafı"
        verbose_name_plural = "Ürün Fotoğrafları"


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='review',  blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    comment = models.TextField()
    show_name = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Yorum"
        verbose_name_plural = "Yorumlar"
    
    def __str__(self):
        return self.title

class AboutUs(models.Model):
    owner_photo = models.ImageField(upload_to='core/img')
    main_text = CKEditor5Field('Text', config_name='extends')
    comment_1 = models.TextField(blank=True, null=True)
    comment_2 = models.TextField(blank=True, null=True)
    comment_3 = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Hakkımızda sayfası içerikleri"

    class Meta:
        verbose_name = "Firma Sayfası"
        verbose_name_plural = "Firma Sayfası"
