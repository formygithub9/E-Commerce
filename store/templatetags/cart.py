from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product_id,cart):
    keys=cart.keys()
    for id in keys:
        if int(id)==product_id:
            return True
    return False

@register.filter(name='quantity')
def quantity(product_id,cart):
    return cart.get(str(product_id))

@register.filter(name='price_total')
def price_total(product,cart):
    return product.price*quantity(product.id,cart)

@register.filter(name='total_cart_price')
def total_cart_price(product,cart):
    sum=0
    for p in product:
       sum+=price_total(p,cart)
    return sum

@register.filter(name='currency')
def currency(number):
    return "₹"+str(number)

       


