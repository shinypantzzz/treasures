from django.test import TestCase
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

from .models import Treasure

# Create your tests here.

class TreasureModelTests(TestCase):
    def test_location_out_of_boundaries(self):
        t = Treasure(location=Point(-91, 145), description="Some description")
        self.assertRaises(ValidationError, t.full_clean)

    def test_normal_location(self):
        t = Treasure(location=Point(45, 145), description="Some description")
        t.full_clean()

    def test_short_description(self):
        t = Treasure(location=Point(45, 145), description="Short")
        self.assertRaises(ValidationError, t.full_clean)

    def test_normal_description(self):
        t = Treasure(location=Point(45, 145), description="Loooong description")
        t.full_clean()