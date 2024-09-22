from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.core.paginator import Paginator
import random


from .models import Product, GeneralCategory, AboutUs
from .forms import ProductFilterForm, ReviewForm

# Create your views here.

class GeneralCategories:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['general_categories'] = GeneralCategory.objects.filter(show_navbar=True).prefetch_related('subcategories')
        return context


class HomepageView(GeneralCategories, ListView):
    model = Product
    template_name = 'core/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Query for best seller products
        context['best_sellers'] = Product.objects.filter(best_seller=True)
        # Query for newest products
        context['newest_products'] = Product.objects.filter(newest=True)
        return context

    
class ProductpageView(HomepageView):
    template_name = 'core/products.html'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.all()

        search_query = self.request.GET.get('query', '')

        # Filter based on the search query
        if search_query:
            queryset = queryset.filter(Q(name__icontains=search_query) | Q(short_description__icontains=search_query))

        form = ProductFilterForm(self.request.GET)
        if form.is_valid():
            selected_bottle_volumes = form.cleaned_data.get('bottle_volume')
            selected_bottle_types = form.cleaned_data.get('bottle_type')
            selected_bottle_color = form.cleaned_data.get('bottle_color')
            selected_cap_types = form.cleaned_data.get('bottle_cap_type')
            selected_categories = form.cleaned_data.get('general_category')
            selected_sub_categories = form.cleaned_data.get('sub_category')

            selected_height = form.cleaned_data.get('height')
            selected_width = form.cleaned_data.get('width')
            selected_diameter = form.cleaned_data.get('diameter')
            selected_depth = form.cleaned_data.get('depth')
            selected_weight = form.cleaned_data.get('weight')

            if selected_bottle_types:
                queryset = queryset.filter(bottle_type__in=selected_bottle_types)
            if selected_bottle_volumes:
                queryset = queryset.filter(bottle_volume__in=selected_bottle_volumes)
            if selected_bottle_color:
                queryset = queryset.filter(bottle_color__in=selected_bottle_color)
            if selected_cap_types:
                queryset = queryset.filter(bottle_cap_type__in=selected_cap_types)
            if selected_categories:
                queryset = queryset.filter(general_category__in=selected_categories)
            if selected_sub_categories:
                queryset = queryset.filter(sub_category__in=selected_sub_categories)
            if selected_height:
                queryset = queryset.filter(height=selected_height)  
            if selected_width:
                queryset = queryset.filter(width=selected_width)  
            if selected_diameter:
                queryset = queryset.filter(diameter=selected_diameter)  
            if selected_depth:
                queryset = queryset.filter(depth=selected_depth)  
            if selected_weight:
                queryset = queryset.filter(weight=selected_weight) 

        # Handle filtering by best sellers and newest
        filter_by = self.request.GET.get('filter_by', '')
        if filter_by == 'best_sellers':
            queryset = queryset.filter(best_seller=True)
        elif filter_by == 'newest':
            queryset = queryset.filter(newest=True)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductFilterForm(self.request.GET or None)
        
        breadcrumbs = [{'name': 'Bütün Ürünler', 'url': '/urunler/'}]

        form = context['form']
        if form.is_valid():
            selected_category = form.cleaned_data.get('general_category')
            selected_sub_category = form.cleaned_data.get('sub_category')
            selected_bottle_volumes = form.cleaned_data.get('bottle_volume')
            selected_bottle_types = form.cleaned_data.get('bottle_type')
            selected_bottle_cap_type = form.cleaned_data.get('bottle_cap_type')
            selected_bottle_color = form.cleaned_data.get('bottle_color')

            if selected_category:
                if len(selected_category) == 1:
                    category = selected_category[0]
                    breadcrumbs.append({'name': str(category), 'url': f"?general_category={category.id}"})
                else:
                    breadcrumbs.append({'name': "Çeşitli Kategoriler", 'url': '#'})

            if selected_sub_category:
                if len(selected_sub_category) == 1:
                    sub_category = selected_sub_category[0]
                    breadcrumbs.append({'name': str(sub_category), 'url': f"?sub_category={sub_category.id}"})
                else:
                    breadcrumbs.append({'name': "Çeşitli Alt Kategoriler", 'url': '#'})
            
            if selected_bottle_types:
                if len(selected_bottle_types) == 1:
                    bottle_type = selected_bottle_types[0]
                    breadcrumbs.append({'name': str(bottle_type), 'url': f"?bottle_type={bottle_type.id}"})
                else:
                    breadcrumbs.append({'name': "Çeşitli Materyal", 'url': '#'})

            if selected_bottle_volumes:
                if len(selected_bottle_volumes) == 1:
                    volume = selected_bottle_volumes[0]
                    breadcrumbs.append({'name': f"{volume}", 'url': f"?bottle_volume={volume.id}"})
                else:
                    volumes_display = " - ".join([f"{volume}" for volume in selected_bottle_volumes[:2]])
                    if len(selected_bottle_volumes) > 2:
                        volumes_display += "..."
                    breadcrumbs.append({'name': f"{volumes_display}", 'url': '#'})

            if selected_bottle_cap_type:
                if len(selected_bottle_cap_type) == 1:
                    bottle_cap_type = selected_bottle_cap_type[0]
                    breadcrumbs.append({'name': str(bottle_cap_type) + ' Ağız Şekli' , 'url': f"?bottle_cap_type={bottle_cap_type.id}"})
                else:
                    breadcrumbs.append({'name': "Çeşitli Ağız Şekli", 'url': '#'})

            if selected_bottle_color:
                if len(selected_bottle_color) == 1:
                    bottle_color = selected_bottle_color[0]
                    breadcrumbs.append({'name': str(bottle_color) + ' Renk', 'url': f"?bottle_color={bottle_color.id}"})
                else:
                    breadcrumbs.append({'name': "Çeşitli Renkler", 'url': '#'})

        # Handle sorting/filtering by best sellers and newest
        filter_by = self.request.GET.get('filter_by', '')
        if filter_by == 'best_sellers':
            breadcrumbs.append({'name': "Çok Satanlar", 'url': '?'})
        elif filter_by == 'newest':
            breadcrumbs.append({'name': "En Yeniler", 'url': '?'})
        
        context['breadcrumbs'] = breadcrumbs

        # Paginate products
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


class ProductpageDetail(GeneralCategories,FormMixin ,DetailView ):
    model = Product
    template_name = 'core/product_detail.html'
    form_class = ReviewForm

    def get_random_products(self, limit=7):
        # Fetch random products excluding the current product
        products = list(Product.objects.exclude(pk=self.get_object().pk))
        return random.sample(products, min(len(products), limit))

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()

        # Get the current product
        current_product = self.get_object()
        
        # Get the IDs of the categories for the current product
        category_ids = current_product.general_category.values_list('id', flat=True)

        # Filter similar products based on matching categories
        similar_products = Product.objects.filter(
            general_category__in=category_ids
        ).exclude(pk=current_product.pk)

        if similar_products.count() < 4:
            # If fewer than 4 similar products, get additional products
            additional_needed = 6 - similar_products.count()
            additional_products = self.get_random_products(limit=additional_needed)
            
            # Combine similar products with additional products to make up 4 products
            context['products_to_display'] = list(similar_products) + list(additional_products)
        else:
            context['products_to_display'] = similar_products

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit=False)
            if form.cleaned_data['show_name'] == 'False':
                review.title = 'Anonim'
            review.product = self.object
            review.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class AboutUsPage(GeneralCategories,DetailView):
    model = AboutUs
    template_name = 'core/about_us.html'
    context_object_name = 'about_us'
    
    def get_object(self):
        return AboutUs.objects.first()
    
