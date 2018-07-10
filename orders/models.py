from django.db import models

# Create your models here.
from shop.models import Product

class Order(models.Model):
	#用户姓名
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    #邮件
    email = models.EmailField()
    #地址
    address = models.CharField(max_length=250)
    #邮编
    postal_code = models.CharField(max_length=20)
    #城市
    city = models.CharField(max_length=100)
    #订单生成时间
    created = models.DateTimeField(auto_now_add=True)
    #更新时间
    updated = models.DateTimeField(auto_now=True)
    #区分支付和未支付订单
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return 'Order {}'.format(self.id)
    #得到订单中购买物品的总花费。    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
        
        
class OrderItem(models.Model):
	#保存物品，数量和每个物品的支付价格
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product,
                    related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return '{}'.format(self.id)
    #得到订单中购买物品的总花费。
    def get_cost(self):
        return self.price * self.quantity
