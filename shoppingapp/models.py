from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class section(models.Model):
    section_name=models.CharField(max_length=100)
    section_image=models.ImageField(upload_to='sectionimg/')

    def __str__(self):
        return self.section_name

class product(models.Model):
    product_name=models.CharField(max_length=100)
    product_img=models.ImageField(upload_to='productimg/')
    product_price=models.IntegerField()
    product_description=models.TextField()
    connection=models.ForeignKey(section,related_name="sections",on_delete=models.CASCADE)


    def __str__(self):
        return self.product_name
    
class detailing(models.Model):
    detail_connection=models.ForeignKey(product,related_name="products",on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    

class completeorder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    House_number = models.PositiveIntegerField()
    Street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    Zip_code = models.IntegerField()
    state=models.CharField(max_length=255)
    Payment_type=models.TextField(max_length=100,
                                  choices=[
                                      ('card','card'),  
                                      ],
                                      default='card'
                                  )

    def __str__(self):
        return f"{self.username} - {self.city}"
    

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"
    

class updateprofile(models.Model):
    username=models.CharField(max_length=255)
    email=models.EmailField()
    password=models.CharField(max_length=255)

    def __str__(self):
        return self.username