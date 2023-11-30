from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView,ListView
from account.models import *
from django.contrib import messages
from .forms import Reviewform
from .models import Review
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.

def signin_requried(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,'Login Required.....')
            return redirect('log')
    return inner

dec=[signin_requried,never_cache]



# class Productdetailsview(TemplateView):
#     template_name="productdet.html"
@method_decorator(dec,name='dispatch')
class Productdetailsview(DetailView):
    template_name="productdet.html"
    pk_url_kwarg="id"
    queryset=Product.objects.all()
    context_object_name="data"

    def get_context_data(self,**kwargs):
        form=Reviewform()
        # print(kwargs,'jk')
        context=super().get_context_data(**kwargs)
        context['form']=form
        pro=kwargs.get('object')
        reviews=Review.objects.filter(product=pro)
        context['review']=reviews
        return context

dec
def addreview(request,*args,**kwargs):
    pid=kwargs.get('id')
    form_data=Reviewform(data=request.POST)
    if form_data.is_valid():
        review=form_data.cleaned_data.get('review')
        product=Product.objects.get(id=pid)
        user=request.user
        Review.objects.create(user=user,review=review,product=product)
        messages.success(request,"Review Added")
        return redirect('prodet',id=pid)
    messages.error(request,"Can't Add review")
    return redirect('prodet',id=pid)



@method_decorator(dec,name='dispatch')     
class Addtocartview(View):
    def get(self,request,**kwargs):
        pid=kwargs.get('id')
        product=Product.objects.get(id=pid)
        user=request.user
        Cart.objects.create(product=product,user=user)
        messages.success(request,"Product is Added To Cart.........")
        return redirect('home')


@method_decorator(dec,name='dispatch')
class Cartlistview(ListView):
    template_name='cart.html'
    queryset=Cart.objects.all()
    context_object_name='cart'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user,status='cart')


@method_decorator(dec,name='dispatch')
class Deletecartitem(View):
    def get(self,request,**kwargs):
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.delete()
        messages.success(request,'Cart Item Removed')
        return redirect('cartlist')


@method_decorator(dec,name='dispatch')
class Checkoutview(View):
    def get(self,request,**kwargs):
        return render(request,"checkout.html")
    def post(self,request,**kwargs):
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        ph=request.POST.get('phone')
        add=request.POST.get('address')
        Order.objects.create(cart=cart,phone=ph,address=add)
        cart.status='Order Placed'
        cart.save()
        messages.success(request,"Order Placed!!")
        return redirect("home")


@method_decorator(dec,name='dispatch')
class Orderlistview(ListView):
    template_name='orderlist.html'
    context_object_name="data"
    queryset=Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user)


dec
def cancelorder(request,*args,**kwargs):
    oid=kwargs.get('id')
    order=Order.objects.get(id=oid)
    order.status="Cancelled"
    order.save()
    messages.success(request,"Order Cancelled")
    return redirect('order')
