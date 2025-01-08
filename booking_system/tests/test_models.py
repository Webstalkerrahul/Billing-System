from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from booking_system.models import Resources, Bookings

class ResourcesModelTest(TestCase):
    def setUp(self):
        self.resource = Resources.objects.create(
            name="Test Resource",
            description="Test Description",
            total_quantity=100,
            available_quantity=100
        )

    def test_resource_creation(self):
        self.assertEqual(self.resource.name, "Test Resource")
        self.assertEqual(self.resource.description, "Test Description")
        self.assertEqual(self.resource.total_quantity, 100)
        self.assertEqual(self.resource.available_quantity, 100)

    def test_negative_total_quantity(self):
        resource = Resources(
            name="Test Resource",
            description="Test Description",
            total_quantity=-1,
            available_quantity=0
        )
        with self.assertRaises(ValidationError):
            resource.full_clean()

    def test_negative_available_quantity(self):
        resource = Resources(
            name="Test Resource",
            description="Test Description",
            total_quantity=100,
            available_quantity=-1
        )
        with self.assertRaises(ValidationError):
            resource.full_clean()

class BookingsModelTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.resource = Resources.objects.create(
            name="Test Resource",
            description="Test Description",
            total_quantity=100,
            available_quantity=50
        )

        self.booking = Bookings.objects.create(
            user=self.user,
            resource=self.resource,
            purchase_quantity=10
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.user, self.user)
        self.assertEqual(self.booking.resource, self.resource)
        self.assertEqual(self.booking.purchase_quantity, 10)
        self.assertTrue(isinstance(self.booking.booking_date, timezone.datetime))

    def test_purchase_quantity_exceeds_available(self):
        booking = Bookings(
            user=self.user,
            resource=self.resource,
            purchase_quantity=60
        )
       
        with self.assertRaises(ValidationError):
            booking.full_clean()