from .models import Category, BagItem


def navbar_data(request):

    categories = Category.objects.all()

    bag_count = 0

    if request.user.is_authenticated:

        bag_items = BagItem.objects.filter(
            user=request.user
        )

        bag_count = sum(
            item.quantity for item in bag_items
        )

    return {
        'navbar_categories': categories,
        'bag_count': bag_count,
    }