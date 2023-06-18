from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect
from account_mgmt.models import *
from .models import *

#Create your views here.

#Seller add product

def add_store(request):
     user = request.user
     if user.is_authenticated and request.method == 'POST':
         seller = Seller.objects.get(seller_id = user.id )
         new_store = Store(
                       store_name = request.POST.get('name'),
                       shed_number = request.POST.get('shed-number'),
                       store_location= "location",
                       gmap_location_link = request.POST.get('gmap-location-link'),
                       seller = Seller.objects.get(seller_id=user.id),
                       market_id = Market.objects.get(id = request.POST.get('market'))
         )
         new_store.save()
         return redirect(reverse('store-list',args=[user.id]))
     return render(request,'addStore.html',{'markets':Market.objects.all()})  
       

def store_list(request,user_id):
    user = request.user
    if user.is_authenticated:
       stores = Store.objects.filter(seller__seller_id=user)
       return render(request,'storeList.html',{'user':user,'stores':stores})
    else:
       return redirect('home')

    
def upload_product(request):
     user = request.user
     if user.is_authenticated:
         seller = Seller.objects.get(seller_id = user )
         stores = Store.objects.filter(seller__seller_id = user)
         if request.method == 'POST':
                seller = Seller.objects.get(seller_id = user.id )
                new_product = Product(
                            photo = request.FILES.get('photo'),
                            product_name = request.POST.get('product-name'),
                            price = request.POST.get('price'),
                            category = request.POST.get('category'),
                            store = Store.objects.get(id=request.POST.get('store') ),
                            description= request.POST.get('description'),
                            quantity = request.POST.get('quantity'),
                            seller = Seller.objects.get(seller_id=user.id),
                )
                new_product.save()
                return redirect(reverse('profile',args=[user.id]))
         context = {'seller':seller,
                    'stores':Store.objects.filter(seller__seller_id=user)}
         return render(request,'addProduct.html',context)  
     else:
        return redirect('home')  
def search(request):
    if request.method == 'POST':
       keyword = request.POST.get('keyword')
       market_id = request.POST.get('market')
       category = request.POST.get('category')
       price_range = float(request.POST.get('price-range'))
       products = Product.objects.filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
       if(market_id):
         market = Market.objects.get( id = int(market_id) )
         products = products.filter(store__market_id=market)
       if(category):
         products = products.filter(Q(category=category))  
       if(price_range):
         products = products.filter(price__lte=price_range)  
      # products = Product.objects.filter(Q(product_name__icontains=keyword),Q( Q(description__icontains=keyword)| Q(Q(category=category)|Q(store__market_id=market)), price__lte=price_range, ))
       context = {'products':products,
                  'keyword':keyword,
                  'user':request.user,
                  'previous_page':request.META.get('HTTP_REFERRER'),
                  
                  }
       return render(request, 'searchResults.html',context)
    return render(request, 'searchForm.html',{'markets':Market.objects.all()})

def product_info(request,product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    context={
        'user':user,
        'product':product
    }
    return render(request,'productInfo.html',context)    


def edit_product_info(request,product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    if not user.is_authenticated or (product is None) or (product.seller.seller_id != user):
     return redirect('home')
    if request.method =='POST':
        product.product_name = request.POST['name']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.category = request.POST['category']
        product.description = request.POST['description']
        product.save()
        return redirect(reverse('product-info',args=[product.id]))
    context={
        'user':user,
        'product':product
    }
    return render(request,'editProductInfo.html',context)      

def delete_product(request,product_id):
    user = request.user
    product = Product.objects.get(id=product_id)
    if not user.is_authenticated or (product is None) or (product.seller.seller_id != user):
     return redirect('home')
    else: 
        product.delete() 
        return redirect(reverse('profile',args=[user.id]))


def how_to_get_gmap_link(request):
    user = request.user
    context={
        'user':user,
    }
    return render(request,'howToGetLink.html',context)  
