from rest_framework import generics, status
from rest_framework.response import Response
from inventory.models import Inventory
from .models import Sales
from .serializers import SalesSerializer


class SalesListView(generics.ListAPIView):
    serializer_class = SalesSerializer

    def get_queryset(self):
        return Sales.objects.filter(franchise=self.request.user.franchise)


class SalesDetailView(generics.RetrieveAPIView):
    serializer_class = SalesSerializer

    def get_queryset(self):
        return Sales.objects.filter(franchise=self.request.user.franchise)


class SaleCreateView(generics.CreateAPIView):
    serializer_class = SalesSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product']
        quantity_sold = serializer.validated_data['quantity_sold']
        franchise = request.user.franchise

        try:
            inventory = Inventory.objects.get(franchise=franchise, product=product_id)
        except Inventory.DoesNotExist:
            return Response({"error": "Inventory not found for the product in your franchise."},
                            status=status.HTTP_400_BAD_REQUEST)

        if inventory.available_quantity < quantity_sold:
            return Response({"error": "Not enough stock available for this sale."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Update the inventory
        inventory.available_quantity -= quantity_sold
        inventory.total_sold += quantity_sold
        inventory.save()

        # Create the sale
        sale = serializer.save(franchise=franchise)

        return Response(SalesSerializer(sale).data, status=status.HTTP_201_CREATED)
