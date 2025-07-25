from django.db import models
from django.utils import timezone

#상품재고DB
class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    productName = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.productName

#회원목록DB
class Member(models.Model):
    no = models.BigAutoField(primary_key=True)
    userId = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.TextField()
    nickname = models.TextField()
    gender = models.TextField()
    email = models.EmailField()
    phoneNumber = models.TextField()
    address = models.TextField()
    joinDate = models.DateTimeField(default=timezone.now)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.userId
    
#장바구니DB
class Cart(models.Model):
    cartOwner = models.OneToOneField(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cartOwner.nickname}의 장바구니"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    productInCart = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
#주문내역DB     더미데이터!
class Order(models.Model):
    orderNumber = models.BigAutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    orderDate = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=30)
    shippingAddress = models.TextField()

    def __str__(self):
        return f"Order #{self.orderNumber} by {self.member.name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.productName} {self.quantity}개 "

#상담게시판DB
class Board(models.Model):
    no = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    showCount = models.IntegerField(default=0)