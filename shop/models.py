from decimal import *
from functools import reduce
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ProductClass(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(default='', blank=True)
    priority = models.IntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'ProductClass'
        verbose_name_plural = 'ProductClasses'
        ordering = ['priority', 'name']

    def __str__(self):
        return str(self.name) + '(' + str(self.slug) + ')'


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(default="nophoto.png")
    description = models.TextField(default='', blank=True)
    priority = models.IntegerField(default=0, blank=True)
    productClass = models.ManyToManyField('ProductClass', blank=True)
    measure = models.CharField(max_length=50, default='шт', blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['priority', 'name']

    def __str__(self):
        return str(self.name) + '(' + str(self.slug) + ')'


class ProductVariant(models.Model):
    name = models.CharField(max_length=100)
    addition = models.CharField(default='', max_length=140)
    slug = models.SlugField(unique=True)
    description = models.TextField(default='', blank=True)
    priority = models.IntegerField(default=0, blank=True)
    image = models.ImageField(default="nophoto.png")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=0, blank=True)
    vendorCode = models.CharField(default=0, max_length=50, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'ProductVariant'
        verbose_name_plural = 'ProductVariants'
        ordering = ['priority', 'name']

    def __str__(self):
        return str(self.name) + '(' + str(self.slug) + ')'

    def getPrice(self, count):
        mn = 0
        mnCount = -1
        for price in self.price_set.all():
            if price.quantity > mnCount and price.quantity <= count:
                mn = price.price
                mnCount = price.quantity
        return mn


class Price(models.Model):
    price = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    quantity = models.IntegerField(default=0, blank=True)
    productVar = models.ForeignKey('ProductVariant', on_delete=models.CASCADE, default=0, blank=True)

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'
        ordering = ['productVar', 'quantity']

    def __str__(self):
        return 'Price:' + str(self.productVar.name) + " : " + str(self.quantity) + " : " + str(self.price)

class SaleSum(models.Model):
    name = models.CharField(max_length=140)
    sale = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    productClasses = models.ManyToManyField('ProductClass', blank=True)
    startSum = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    customers = models.ManyToManyField('auth.Group', blank=True)

    class Meta:
        verbose_name = 'SaleSum'
        verbose_name_plural = 'SalesSum'
        ordering = ['sale', 'name']

    def __str__(self):
        return 'SSale:' + str(self.name) + '(' + str(self.sale) + ')'

    def forUser(self, user):
        return any(map((lambda x: user in x.user_set.all()), self.customers.all()))

    def forProduct(self, product):
        return len(product.product.productclass_set.all().intersect()) != 0

    def checkOrder(self, order):
        if not forUser(order.user):
            return False
        sm = reduce(
            (lambda a, b: a + b),
            map(
                (lambda item: Decimal(item.price) * Deciamal(item.quantity)),
                order.items.objects.all()
            )
        )

        return sm >= startSum


class SaleQuantity(models.Model):
    name = models.CharField(max_length=140)
    sale = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    productClasses = models.ManyToManyField('ProductClass', blank=True)
    startQuantity = models.IntegerField(default=0, blank=True)
    customers = models.ManyToManyField('auth.Group', blank=True)

    class Meta:
        verbose_name = 'SaleQuantity'
        verbose_name_plural = 'SalesQuantity'
        ordering = ['sale', 'name']

    def __str__(self):
        return 'QSale:' + str(self.name) + '(' + str(self.sale) + ')'

    def checkOrder(self, order):
        if not forUser(order.user):
            return False
        sm = reduce(
            (lambda a, b: a + b),
            map(
                (lambda item: item.quantity),
                order.items.objects.all()
            )
        )
        return sm >= startQuantity


class Organisation(models.Model):
    inn = models.CharField(max_length=20, default='', blank=True)
    kpp = models.CharField(max_length=20, default='', blank=True)
    address = models.CharField(max_length=250, default='', blank=True)
    name = models.CharField(max_length=250, default='', blank=True)
    owners = models.ManyToManyField('auth.User', blank=True)

    class Meta:
        verbose_name = 'Organisation'
        verbose_name_plural = 'Organisations'
        ordering = ['inn']

    def __str__(self):
        return 'Organisation:' + str(self.name) + '(' + str(self.inn) + ')'


class SellerOrganisation(models.Model):
    inn = models.CharField(max_length=20, default='', blank=True)
    kpp = models.CharField(max_length=20, default='', blank=True)
    address = models.CharField(max_length=250, default='', blank=True)
    name = models.CharField(max_length=250, default='', blank=True)
    owners = models.ManyToManyField('auth.User', blank=True)
    bik = models.CharField(max_length=50, default='', blank=True)
    corAcc = models.CharField(max_length=250, default='', blank=True)
    bank = models.CharField(max_length=250, default='', blank=True)
    checkACC = models.CharField(max_length=50, default='', blank=True)

    class Meta:
        verbose_name = 'SellerOrganisation'
        verbose_name_plural = 'SellerOrganisations'
        ordering = ['inn']

    def __str__(self):
        return 'SellerOrganisation:' + str(self.name) + '(' + str(self.inn) + ')'


class OrderItem(models.Model):
    product = models.ForeignKey('ProductVariant', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True)
    price = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True) # price per one
    order = models.ForeignKey('Order', on_delete=models.SET_NULL, related_name='items', related_query_name='items', blank=True, null=True)

    class Meta:
        verbose_name = 'OrderItem'
        verbose_name_plural = 'OrderItems'
        #ordering = ['product']

    def __str__(self):
        return 'OrderItem:' + str(self.product) + ' ' + str(self.quantity)

    def getSum(self):
        #print(Decimal(self.price), int(self.quantity))
        return Decimal(self.price) * int(self.quantity)


class OrderStatus(models.Model):
    name = models.CharField(max_length=250, default='', blank=True)
    color = models.CharField(max_length=200, default='', blank=True)

    class Meta:
        verbose_name = 'OrderStatus'
        verbose_name_plural = 'OrderStatuses'
        ordering = ['name']


    def __str__(self):
        return self.name + ' (' + self.color + ')'


class Order(models.Model):
    datetime = models.DateTimeField(null=True, blank=True)
    #organisation = models.ForeignKey('Organisation', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('auth.user', on_delete=models.SET_NULL, null=True)
    #items = models.ManyToManyField('OrderItem', blank=True)
    #active = models.BooleanField(default=False, blank=True)
    #finished = models.BooleanField(default=False, blank=True)
    #cancelled = models.BooleanField(default=False, blank=True)
    status = models.ForeignKey('OrderStatus', on_delete=models.SET_NULL, blank=True, null=True)
    sale = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    invoice = models.OneToOneField('Invoice', on_delete=models.SET_NULL, null=True, blank=True, parent_link=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['datetime']

    def __str__(self):
        return 'Order:' + str(self.datetime)
        + ' by ' + str(self.organisation)
        + ' status:' + str(self.status.name)

    def activate(self):
        #self.finished = False
        #self.active = True
        #self.cancelled = False
        self.status=OrderStatus.objects.get(pk=2)
        self.datetime = timezone.now()
        self.save()

    def finish(self):
        #self.finished = True
        #self.active = False
        #self.cancelled = False
        self.status=OrderStatus.objects.get(pk=3)
        self.save()

    def cancel(self):
        #self.finished = False
        #self.active = False
        #self.cancelled = True
        self.status=OrderStatus.objects.get(pk=4)
        self.save()

    def delZeroes(self):
        self.items.remove(*self.items.filter(quantity=0))
        self.save()

    def getItemByProduct(self, product):
        '''
        Arguements:
        1) product -- instance of the ProductVariant

        Return:
        1) None -- if there is no such product
        2) OrderItem -- otherwise
        '''
        pItems = self.items.filter(product=product)
        if len(pItems) == 0:
            return None
        else:
            return pItems[0]

    def getQuantity(self, product):
        '''
        Arguements:
        1) product -- instance of the ProductVariant

        Return:
        1) quantity of product in order
        '''
        pItem = self.getItemByProduct(product)
        if pItem is None:
            return 0
        else:
            return pItem.quantity

    def getPrice(self, product):
        '''
        Arguements:
        1) product -- instance of the ProductVariant

        Return:
        1) price (per one) of product in order
        2) None if there is no such product
        '''
        pItem = self.getItemByProduct(product)
        if pItem is None:
            return None
        else:
            return pItem.price

    def setQuantity(self, product, quantity):
        '''
        Arguements:
        1) product -- instance of the ProductVariant
        2) quantity -- int

        Return:
        nothing
        '''
        pItem = self.getItemByProduct(product)
        if pItem is None:
            self.items.create(product=product, quantity=quantity, price=0)
            self.updatePrice(product)
        else:
            pItem.quantity = quantity
            pItem.save()
            self.updatePrice(product)


    def setPrice(self, product, price):
        '''
        Arguements:
        1) product -- instance of the ProductVariant
        2) price -- decimal

        Return:
        nothing
        '''
        pItem = self.getItemByProduct(product)
        if pItem is None:
            self.items.create(product=product, quantity=0, price=price)
        else:
            pItem.price = price
            pItem.save()

    def updatePrice(self, product):
        pItem = self.getItemByProduct(product)
        self.setPrice(product, product.getPrice(pItem.quantity))

    def getTotalSum(self):
        return sum(map(
                (lambda a: Decimal(a.price) * Decimal(a.quantity)),
                self.items.all()
            ))

    def getTotalQuantity(self):
        return reduce(
                (lambda a, b:
                    a.quantity + b.quantity),
                self.items.all()
            )

    def applySale(self, sale):
        pass

    def getDelivery(self):
        sm = self.getTotalSum()
        dSum = Decimal('inf');
        # for is bad; I will replace it with reduce
        for item in Delivery.objects.all():
            if item.minSum <= sm:
                dSum = min(dSum, item.price)
        return dSum

    def checkOrder(self):
        '''
        checks if order sum is enough to make order
        '''
        return self.getTotalSum() >= ShopConstant.getMinOrderSum()


class Delivery(models.Model):
    minSum = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    price = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Delivery'
        ordering = ['price']

    def __str__(self):
        return "delivery"


class Invoice(models.Model):
    date = models.DateTimeField(null=True,blank=True)
    seller = models.ForeignKey('SellerOrganisation', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    customer = models.ForeignKey('Organisation', on_delete=models.SET_NULL, null=True, blank=True)
    personInCharge = models.CharField(max_length=250, default='', blank=True)
    shipAddress = models.CharField(max_length=250, default='', blank=True)
    comment = models.TextField(default='', blank=True)
    taxes = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)
    deliverySum = models.DecimalField(max_digits=50, decimal_places=2, default=0, blank=True)

    def calculateDelivery(self):
        self.deliverySum = self.order.getDelivery()
        self.save()

    def calculateTaxes(self):
        self.taxes = Decimal(((self.order.getTotalSum() + self.deliverySum) * Decimal(0.18) / Decimal(1.18)).quantize(Decimal('.01'), rounding=ROUND_CEILING))
        self.save()

    def recalc(self):
        self.calculateDelivery()
        self.calculateTaxes()

    def toPay(self):
        return self.order.getTotalSum() + self.deliverySum


class ShopConstant(models.Model):
    name = models.CharField(max_length=140, default='', unique=True)
    value = models.CharField(max_length=140, default='')
    comment = models.CharField(max_length=200, default='')

    def getField(fieldName):
        return ShopConstant.objects.get(name=fieldName).value

    def getShopName():
        return ShopConstant.getField('shopname')

    def getMinOrderSum():
        return Decimal(ShopConstant.getField('minordersum'))
