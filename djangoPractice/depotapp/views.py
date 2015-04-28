# -*- coding: utf-8 -*-

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.core import serializers

import datetime
# app specific files

from models import *
from forms import *


def hello(request):
    return HttpResponse("hello, Django!")

def store_view(request):
    products = Product.objects.filter(date_available__gt = datetime.datetime.now().date())#.order_by("-date_available")
    print "-->product %s" %(products)
    
    t = get_template('depotapp/store.html')
    c = RequestContext(request, locals())
    
    return HttpResponse(t.render(c))

def view_cart(request):
    cart = request.session.get("cart", None)
    
    t = get_template('depotapp/view_cart.html')
    
    if not cart:
        cart = Cart()     
        
    print "--> cart %s" %(cart)
    
#     serialized_cart = cart.__dict__
#     serialized_cart = serializers.serialize('json', [cart])
         
    request.session["cart"] = cart
    
    c = RequestContext(request,locals())
    return HttpResponse(t.render(c))

def add_to_cart(request):
    product = Product.objects.get(id = id)
    cart = request.session.get("cart",None)
    
    if not cart:
        cart = Cart()
        
    request.session['cart'] = cart
    
    cart.add_product(product)
    
    # 从session中获取对象后，对该对象属性的更改不能自动同步到session中
    # 而是需要重新写入session
    request.session['cart'] = cart
    
    return view_cart(request)

def clean_cart(request):
    request.session['cart'] = Cart()
    return view_cart(request)

def create_product(request):
    print "--> create_product"
    
    form = ProductForm(request.POST or None)
     
    print "--> ProductForm ready"
     
    if form.is_valid():
        form.save()
        form = ProductForm()
 
    t = get_template('depotapp/create_product.html')
    c = RequestContext(request, locals())
    
    return HttpResponse(t.render(c))

def submit_product(request):
    print request.POST
 
    product_model = request.POST.get('Product')
    Product.objects.create(
        title = request.POST.get('title'),
        description = request.POST.get('description'),
        image_url = request.POST.get('image_url'),
        price = request.POST.get('price'),
        date_available = request.POST.get('date_available'),
    )
    bbs_content = request.POST.get('content')
#     return HttpResponse('Your product information has been submitted!')
#     return HttpResponseRedirect('list_product')
    return list_product(request)
    
def list_product(request):
    print "--> list_product"
    
    # Paginator implementation
    list_items = Product.objects.all()
    
    print "--> list_items 1", type(list_items), list_items
    
    print "| title | description | image_url | price"
    
#     for item in list_items:
#         print item.price, type(item.price)
#         print item.title, type(item.title)
#         print "| %s |  %s   | %s | %s" %(item.title, item.description, item.image_url, item.price)

    paginator  = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except :
        list_items = paginator.page(paginator.num_pages)
        
    print "--> list_items 2", type(list_items), list_items
    
#     title_list = []
#     for item in list_items:
#         title_list.append(item.title)
#     list_items = title_list
#     print "--> list_items 3", type(list_items), list_items
    
    t = get_template('depotapp/list_product.html')
    c = RequestContext(request, locals()) 
#     print "-->[%s]%s" %(type(c), str(c))
#     print "-->%s" %(c[1]['list_items'])
    return HttpResponse(t.render(c))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def category(request, cate_id):
#     bbs_list = models.BBS.objects.filter(category__id = cate_id)
#     bbs_categories = models.Category.objects.all()
#     
#     return render_to_response('index.html',{
#                                             'bbs_list':bbs_list,
#                                             'user':request.user,
#                                             'bbs_category':bbs_categories,
#                                             'category_id':int(cate_id)
#                                             })
# 
# def bbs_detail(request, bbs_id):
#     bbs_obj = models.BBS.objects.get(id = bbs_id)
#     return render_to_response('bbs_detail.html', {'bbs_obj':bbs_obj,'user':request.user}, context_instance = RequestContext(request))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def view_product(request, id):
    print "--> view_product"
    product_instance = Product.objects.get(id = id)
    
    t = get_template('depotapp/view_product.html')
    c = RequestContext(request, locals()) 
#     print "-->list_items %s" %(c[1]['list_items'])
    return HttpResponse(t.render(c))

def edit_product(request, id):
    print "--> edit_product"
    product_instance = Product.objects.get(id = id)

    form = ProductForm(request.POST or None, instance = product_instance)

    if form.is_valid():
        form.save()

    t = get_template('depotapp/edit_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))
