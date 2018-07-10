from decimal import Decimal
from django.conf import settings
from shop.models import Product
#购物车类
class Cart(object):
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			#保存一个空的购物车在session中
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def __iter__(self):
		product_ids = self.cart.keys()
		#获取商品并加入到购物车中
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def add(self,product,quantity=1,update_quantity=False):
		#向购物车添加产品或更新其数量	
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity':0,
									 'price':str(product.price)}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def save(self):
		#更新购物车session
		self.session[settings.CART_SESSION_ID] = self.cart
		#将会话标记为“修改”以确保它已被保存。
		self.session.modified = True

	def remove(self,product):
		#将商品移出购物车
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def __len__(self):
		#返回购物车中商品的数量
		return sum(item['quantity'] for item in self.cart.values())

	def get_total_price(self):
		#计算购物车中物品的总价
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def clear(self):
		#清空购物车会话
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True