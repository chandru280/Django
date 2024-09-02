from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Rating
from .forms import RatingForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Fetches the product with the given primary key (pk). If not found, it raises a 404 error.
    ratings = product.ratings.all()  # Retrieves all ratings related to this product.
    average_rating = product.average_rating()  # Calls the `average_rating` method from the `Product` model to calculate the average rating.
    user_rating = None  # Initialize a variable to hold the current user's rating, if it exists.

    if request.user.is_authenticated:  # Checks if the user is logged in.
        user_rating = Rating.objects.filter(product=product, user=request.user).first()  # Retrieves the user's existing rating for this product, if it exists.

    if request.method == 'POST':  # If the form is submitted (HTTP POST request).
        form = RatingForm(request.POST, instance=user_rating)  # Bind the form with the POST data. If `user_rating` exists, the form will update it.
        if form.is_valid():  # Validates the form data.
            rating = form.save(commit=False)  # Create a `Rating` instance, but don't save it to the database yet.
            rating.product = product  # Assign the product to the rating.
            rating.user = request.user  # Assign the current user to the rating.
            rating.save()  # Save the rating to the database.
            return redirect('product_detail', pk=product.pk)  # Redirect to the same product detail page after saving the rating.

    else:  # If the request is not a POST request (usually GET), just display the form.
        form = RatingForm(instance=user_rating)  # Initialize the form. If `user_rating` exists, the form will be pre-filled with the existing data.

    return render(request, 'product_detail.html', {
        'product': product,
        'ratings': ratings,
        'average_rating': average_rating,
        'form': form
    })

@login_required
def add_rating(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.product = product
            rating.user = request.user
            rating.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = RatingForm()

    return render(request, 'add_rating.html', {'form': form, 'product': product})
