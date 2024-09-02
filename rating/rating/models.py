from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Product(models.Model):
    name = models.CharField(max_length=100)  # Product name
    description = models.TextField()  # Product description
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Product price

    def __str__(self):
        return self.name  # Returns the product name as the string representation

    def average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']  # Calculate the average rating for this product using Django's ORM.
        return round(avg_rating, 2) if avg_rating else 0  # Return the average rating rounded to 2 decimal places, or 0 if there are no ratings.



class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')  # Links the rating to a product.
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the rating to a user.
    description = models.TextField(blank=True, null=True)  # Optional text field for the rating description.
    rating = models.PositiveIntegerField(choices=((1, '1 star'), (2, '2 stars'), (3, '3 stars'), (4, '4 stars'), (5, '5 stars')))  # The actual rating value (1-5).
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the field to the current date and time when the rating is created.

    class Meta:
        unique_together = ('product', 'user')  # Ensures that a user can rate a product only once.

    def __str__(self):
        return f"{self.user}'s {self.rating}-star rating for {self.product}"  # String representation of the rating.

