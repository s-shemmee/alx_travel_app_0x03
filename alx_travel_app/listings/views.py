from rest_framework import viewsets
from .models import Listing
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Add serializer_class if you create a serializer for this model
