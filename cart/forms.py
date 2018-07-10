from django import forms

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,21)]
#用户选择商品的表单
class CartAddProductForm(forms.Form):
	#让用户可以在 1~20 之间选择产品的数量。
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,coerce=int)
	update = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
