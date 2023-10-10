from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from .models import Category, Product, Review, Order, ShippingAddress, Payment, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, OrderSerializer, ShippingAddressSerializer, PaymentSerializer, ProductImageSerializer

# Category Views
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_list(request):
    if request.GET.get("sort", None):
        categorys = Category.objects.all().filter(parent=None)
        data = CategorySerializer(categorys, many=True).data
        i = 0
        for category in categorys:
            subcategorys = Category.objects.all().filter(parent=category)
            sct = CategorySerializer(subcategorys, many=True).data
            data[i]["sub"] = sct
            i += 1
        return Response(data)
        
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def category_detail(request, cid):
    try:
        category = Category.objects.get(id=cid)
    except Category.DoesNotExist:
        return Response({"detail": "not found"},status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category)
    if category.parent != None:
        return Response(serializer.data)
    else:
        data = serializer.data
        subcategorys = Category.objects.all().filter(parent=category)
        sctg = CategorySerializer(subcategorys, many=True).data
        data["sub"] = sctg
        return Response(data)
                       

# Product Views (similar structure as Category Views)
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        images = ProductImage.objects.filter(product=product)
        review = Review.objects.filter(product=product)
    except Product.DoesNotExist as e:
        return Response({"detail": str(e)},status=status.HTTP_404_NOT_FOUND)

    try:
        serializer = ProductSerializer(product).data
        imgs = ProductImageSerializer(images, many=True).data
        rvws = user_review(review)
        serializer["images"] = imgs
        serializer["reviews"] = rvws
        return Response(serializer)
    except Exception as e:
        return Response({"detail": str(e)},status=status.HTTP_400_BAD_REQUEST)



# Review Views (similar structure as Category Views)
def user_review(reviews):
    rvw = ReviewSerializer(reviews, many=True).data
    for i in range(len(rvw)):
        user = User.objects.get(id=rvw[i]["user"])
        rvw[i]["user"] = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email}
        
    return rvw

@api_view(['GET', "POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def review_list(request):
    if request.method == 'GET':            
        reviews = Review.objects.all()
        rws = user_review(reviews)
        return Response(rws)

    elif request.method == 'POST':
        data = request.data.copy()
        data["user"] = request.user.pk
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist as e:
        return Response({"detail": str(e)},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(review).data
        user = User.objects.get(id=serializer["user"])
        serializer["user"] = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email}
        return Response(serializer)


# Order Views (similar structure as Category Views)
# ...

# ShippingAddress Views (similar structure as Category Views)
# ...

# Payment Views (similar structure as Category Views)
# ...
