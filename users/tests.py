from django.test import TestCase
from django.contrib.auth import get_user_model

class UserAccountTests(TestCase):

    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'janne', 'password', 'testuser@super.com', 'Labname', 'clinics', 'AT', 'Sbg'
        )
        self.assertEqual(super_user.user_name, 'janne')
        self.assertEqual(super_user.password, 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.laboratory_name, 'Labname')
        self.assertEqual(super_user.laboratory_name, 'Hospital')
        self.assertEqual(super_user.country, 'AT')
        self.assertEqual(super_user.city, 'Sbg')

        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', user_name='janne', laboratory_name='Labname', clinics='Hospital', country='AT', city='Sbg', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='testuser@super.com', user_name='janne', laboratory_name='Labname', clinics='Hospital', country='AT', city='Sbg', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='janne', laboratory_name='Labname', country='AT',
                city='Sbg', password='password', is_superuser=True)

    def test_new_user(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'janne', 'password', 'testuser@super.com', 'Labname', 'clinics', 'AT', 'Sbg'
        )
        self.assertEqual(super_user.user_name, 'janne')
        self.assertEqual(super_user.password, 'password')
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.laboratory_name, 'Labname')
        self.assertEqual(super_user.laboratory_name, 'Hospital')
        self.assertEqual(super_user.country, 'AT')
        self.assertEqual(super_user.city, 'Sbg')
        self.assertFalse(super_user.is_superuser)
        self.assertFalse(super_user.is_staff)
        self.assertFalse(super_user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', user_name='a', laboratory_name='Labname', clinics='Hospital', country='AT',
                city='Sbg', password='password')
