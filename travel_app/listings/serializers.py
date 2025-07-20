from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    
    host = UserSerializer(read_only=True)
    host_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='host', 
        write_only=True
    )
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 
            'host', 
            'host_id',
            'name', 
            'description', 
            'location', 
            'pricepernight', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['listing_id', 'created_at', 'updated_at']

    def validate_pricepernight(self, value):
        """Validate that price per night is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price per night must be greater than zero.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    
    property = ListingSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), 
        source='property', 
        write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 
            'property', 
            'property_id',
            'user', 
            'user_id',
            'start_date', 
            'end_date', 
            'total_price', 
            'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']

    def validate(self, data):
        """Custom validation for booking dates"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError("End date must be after start date.")
                
            # Check for overlapping bookings
            property_obj = data.get('property')
            if property_obj:
                overlapping_bookings = Booking.objects.filter(
                    property=property_obj,
                    start_date__lt=end_date,
                    end_date__gt=start_date
                )
                
                # Exclude current instance if updating
                if self.instance:
                    overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)
                
                if overlapping_bookings.exists():
                    raise serializers.ValidationError("This property is already booked for the selected dates.")
        
        return data

    def validate_total_price(self, value):
        """Validate that total price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Total price must be greater than zero.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    
    property = ListingSerializer(read_only=True)
    property_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(), 
        source='property', 
        write_only=True
    )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), 
        source='user', 
        write_only=True
    )
    
    class Meta:
        model = Review
        fields = [
            'review_id', 
            'property', 
            'property_id',
            'user', 
            'user_id',
            'rating', 
            'comment', 
            'created_at'
        ]
        read_only_fields = ['review_id', 'created_at']

    def validate_rating(self, value):
        """Validate that rating is between 1 and 5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        """Custom validation to ensure one review per user per property"""
        property_obj = data.get('property')
        user_obj = data.get('user')
        
        if property_obj and user_obj:
            existing_review = Review.objects.filter(
                property=property_obj,
                user=user_obj
            )
            
            # Exclude current instance if updating
            if self.instance:
                existing_review = existing_review.exclude(pk=self.instance.pk)
            
            if existing_review.exists():
                raise serializers.ValidationError("You have already reviewed this property.")
        
        return data
