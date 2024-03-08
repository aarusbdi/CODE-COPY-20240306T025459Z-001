from django.views.generic import ListView, DetailView
from django.shortcuts import render

from DjangoEcommerceApp.models import Products, Categories, SubCategories


class BuyerHomeView(ListView):
    template_name = "templates_tailwind/home.html"

    def get_queryset(self):
        return {}

    # def get_context_data(self, **kwargs):
    #     context = super(CategoriesListView, self).get_context_data(**kwargs)
    #     context["filter"] = self.request.GET.get("filter", "")
    #     context["orderby"] = self.request.GET.get("orderby", "id")
    #     context["all_table_fields"] = Categories._meta.get_fields()
    #     return context


class BuyerShopView(ListView):
    template_name = "templates_tailwind/shop.html"

    def get_queryset(self):
        return []

    def get_context_data(self, **kwargs):
        search_params = self.request.GET
        sub_category = search_params.get('sub_category')
        print(sub_category)
        if not sub_category:
            products = Products.objects.all()
        else:
            products = Products.objects.filter(subcategories_id=sub_category)
        categories = Categories.objects.all()

        return {
            'products': [
                {
                    'id': p.pk,
                    'name': p.product_name,
                    'image_url': p.url_slug,
                    'max_price': p.product_max_price,
                    'discount': f"{(int(p.product_max_price) - int(p.product_discount_price)) / 100}%",
                    'price': int(p.product_max_price) - (int(p.product_discount_price) / 100 * int(p.product_max_price))
                } for p in products if p.is_verified],
            'categories': [
                {
                    **category,
                    'show_sub': len(category['sub_categories']) > 0,
                } for category in
                [{
                    'name': category.title,
                    'sub_categories': SubCategories.objects.filter(category_id=category.pk),
                } for category in categories]
            ],
        }


def BuyerShopDetail(request, pk):
    product = Products.objects.get(pk=pk)
    return render(request, 'templates_tailwind/product-detail.html', context={'product': product})
