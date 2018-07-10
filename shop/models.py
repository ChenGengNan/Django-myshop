from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=200,db_index=True)#商品类名
	slug = models.SlugField(max_length=200,db_index=True,unique=True)#用来为这个产品类建立与产品的联系
	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('shop:product_list_by_category',args=[self.slug])
#商品类与商品属于多对一的关系，一个产品可以属于一个分类，一个分类也可包含多个产品。

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products')#商品归属类
	name = models.CharField(max_length=200, db_index=True)#商品名称
	slug = models.SlugField(max_length=200, db_index=True)#用来为这个产品建立与产品类的联系
	image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)#商品图片，可选
	description = models.TextField(blank=True)#商品描述，可选
	price = models.DecimalField(max_digits=10, decimal_places=2)#价格
	stock = models.PositiveIntegerField()#库存
	available = models.BooleanField(default=True)#商品是否可购买
	created = models.DateTimeField(auto_now_add=True)#当对象被创建时这个字段被保存
	updated = models.DateTimeField(auto_now=True)#当对象最后一次被更新时这个字段被保存。

	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('shop:product_detail',args=[self.id,self.slug])
