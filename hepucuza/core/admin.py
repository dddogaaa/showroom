from django import forms
from django.contrib import admin
from .models import *

class ProductForm(forms.ModelForm):
    bottle_volume = forms.ModelChoiceField(queryset=BottleVolume.objects.all(), required=True,label='Hacim' )
    bottle_type = forms.ModelChoiceField(queryset=BottleType.objects.all(), required=True, label='Materyal')
    bottle_color = forms.ModelChoiceField(queryset=BottleColor.objects.all(), required=True, label='Renk')
    bottle_cap_type = forms.ModelChoiceField(queryset=BottleCapType.objects.all(), required=True, label='Ağız Şekli')
    
    general_category = forms.ModelMultipleChoiceField(queryset=GeneralCategory.objects.all(), required=True, widget=forms.CheckboxSelectMultiple, label='Ana Kategori' )
    sub_category = forms.ModelMultipleChoiceField(
        queryset=SubCategory.objects.all(), 
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Alt Kategori'
    )

    class Meta:
        model = Product
        fields = ['product_code','name','short_description','price','notes','long_description','general_category', 'sub_category','bottle_type', 'bottle_volume', 'bottle_cap_type','bottle_color','height','width','diameter','depth','weight','best_seller','newest']

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    inlines = [ProductImageInline]  
    list_display = ('name','short_description', 'best_seller','newest')
    list_filter = ('best_seller', 'newest')
    search_fields = ('name', 'short_description')
    ordering = ['name', 'short_description']

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1  # Number of empty forms displayed to add new subcategories

@admin.register(GeneralCategory)
class GeneralCategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name','show_navbar']
    inlines = [SubCategoryInline]  # Add subcategories inline


@admin.register(BottleType)
class BottleTypeAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name']

@admin.register(BottleVolume)
class BottleVolumeAdmin(admin.ModelAdmin):
    ordering = ['volume']
    list_display = ['volume']

@admin.register(BottleCapType)
class BottleCapTypeAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name']

@admin.register(BottleColor)
class BottleColorAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ['name']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product','title', )
    list_filter = ('show_name',)
    search_fields = ('title', 'comment')
    readonly_fields = ('title', 'comment', 'show_name')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False  # Disable change permissions for all users

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if AboutUs.objects.exists():
            return False
        return super().has_add_permission(request)