from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product, Cart, CartItem
from .serializers import  CartSerializer, CartItemSerializer

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_cart(request):
    if request.method == "GET":
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            items = CartItem.objects.all().filter(cart=cart)
            serializer = CartItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    elif request.method == "POST":
        try:
            product_id = request.data.get('product')
            quantity = request.data.get('quantity', 1)
            cart, created = Cart.objects.get_or_create(user=request.user)
            product = Product.objects.get(pk=product_id)
            existing_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                existing_item.quantity += int(quantity)
                existing_item.save()
            
            return Response({'message': 'Item added to cart successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)



@api_view(['GET', "PUT", "DELETE"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def cart_item(request, item_id):
    if request.method == "PUT":
        try:
            quantity = request.data.get('quantity', 1)
            cart_item = CartItem.objects.filter(cart__user=request.user).get(pk=item_id)
            cart_item.quantity = int(quantity)
            cart_item.save()
            
            return Response({'message': 'Cart item updated successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    elif request.method == "DELETE":
        try:
            cart_item = CartItem.objects.filter(cart__user=request.user).get(pk=item_id)
            cart_item.delete()
            
            return Response({'message': 'Cart item removed successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    else:
        try:
            cart_item = CartItem.objects.filter(cart__user=request.user).get(pk=item_id)
            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)
