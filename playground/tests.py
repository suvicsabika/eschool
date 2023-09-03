from django.test import TestCase
from .models import People

class PeopleModelTest(TestCase):
    def test_full_name(self):
        student = People(first_name='John', last_name='Doe')
        self.assertEqual(student.first_name + ' ' + student.last_name + ' - ' + student.role, 'John Doe - Student')
