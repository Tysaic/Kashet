from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.db.models import Q
from datetime import date, datetime, timezone
from .models import (Budget, BudgetFile, Department)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import uuid
import os
import tempfile


class BudgetModelTest(TestCase):

    def setUp(self):
        self.dept_wom = Department.objects.create(id=1, name='WOM')
        self.dept_entel = Department.objects.create(id=2, name='ENTEL')
        self.dept_movistar = Department.objects.create(id=3, name='MOVISTAR')
        self.dept_galpon = Department.objects.create(id=4, name='GALPON')
        
        self.budget = Budget.objects.create(
            title = "Marketing Budget 01 Testing",
            description = "Social media and campaings",
            total_mount = 1500.0,
            currency = "CLP",
            identifier = uuid.uuid4(),
            due_date = datetime(2025, 11, 30, 0, 0, tzinfo=timezone.utc),
            updated = datetime.today(),
            department = self.dept_wom
        )
    
    def test_budget_creation(self):
        """Ensure the budget object is created correctly."""
        today = datetime.today()
        self.assertEqual(self.budget.title, "Marketing Budget 01 Testing")
        self.assertEqual(self.budget.description, "Social media and campaings")
        self.assertEqual(self.budget.total_mount, 1500.0)
        self.assertEqual(self.budget.currency, "CLP")
        #self.assertEqual(self.budget.created_at, today)
        self.assertEqual(self.budget.due_date, datetime(2025, 11, 30, 0, 0, tzinfo=timezone.utc))
        #self.assertEqual(self.budget.updated, today)
        self.assertEqual(self.budget.type, Budget.TYPE_OF_BUDGET[0][0])
        self.assertEqual(self.budget.department, self.dept_wom)
        self.assertIsInstance(self.budget.identifier, uuid.UUID)
    
    def test_budget_model_str(self):
        expected = "Marketing Budget 01 Testing - Social media and campaings - (1500.0 CLP)"
        self.assertEqual(str(self.budget), expected)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())     
class BudgetFileModelTest(TestCase):

    def setUp(self):
        self.dept = Department.objects.create(id=1, name="WOM")
        self.budget = Budget.objects.create(
            title = "File Uploader 1",
            description = "File uploader description 1",
            total_mount = 2000.0,
            currency = "CLP",
            identifier = uuid.uuid4(),
            due_date = datetime(2026, 11, 30, 0, 0, tzinfo=timezone.utc),
            department = self.dept,
        )
    
        self.file = SimpleUploadedFile(
            "test_document.pdf",
            b"dummy file content",
            content_type="application/pdf"
        )

        self.budget_file = BudgetFile.objects.create(
            budget = self.budget,
            file=self.file
        )

    def test_file_upload_relation(self):
        self.assertEqual(self.budget.upload_folders.count(), 1)
        self.assertEqual(self.budget.upload_folders.first().file.name.split('/')[-1], "test_document.pdf")
    
    def test_budgetfile_str(self):
        filename = self.budget_file.file.name.split('/')[-1]
        self.assertEqual(str(self.budget_file), f"budgets/{self.budget.identifier}/{filename}")
    

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BudgetViewTest(TestCase):

    def setUp(self):

        self.dept_wom = Department.objects.create(id=1, name='WOM')
        self.dept_entel = Department.objects.create(id=2, name='ENTEL')
        self.dept_movistar = Department.objects.create(id=3, name='MOVISTAR')
        self.dept_galpon = Department.objects.create(id=4, name='GALPON')
        self.client = Client()
        self.url = reverse('app:add_budget')
    
    def test_add_budget_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/budgets/add_budget.html')
    

    def test_add_budget_post(self):
        data = {
            'title' : 'Title Example',
            'description' : 'Description example lorem ipsum...',  
            'total_mount': 50000,
            'currency': 'CLP',
            'due_date': datetime(2025, 12, 31, 0, 0, tzinfo=timezone.utc),
            'type': '2',
            'department': '3'
        }

        response = self.client.post(self.url, data)
        
        # Redirecting to success_url
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:list_budget'))

        #Verifing budget was created
        budget_test = Budget.objects.filter(
            Q(title__icontains='Title Example') & Q(description__icontains='Description example lorem ipsum...')
        ).first()

        self.assertEqual(budget_test.title, data["title"])
        self.assertEqual(budget_test.description, data["description"])
        self.assertEqual(budget_test.total_mount, data["total_mount"])
        self.assertEqual(budget_test.currency, data["currency"])
        self.assertEqual(budget_test.due_date, data["due_date"])
        self.assertEqual(budget_test.type, Budget.TYPE_OF_BUDGET[1][0])
        self.assertEqual(budget_test.department, self.dept_movistar)
        self.assertIsNotNone(budget_test.identifier)
        self.assertIsInstance(budget_test.identifier, uuid.UUID)
    
    def test_add_budget_post_single_file(self):
        dummy_file = SimpleUploadedFile(            
            "test_document.pdf",
            b"dummy file content",
            content_type="application/pdf"
        )

        data = {
            'title' : 'Title Example',
            'description' : 'Description example lorem ipsum...',  
            'total_mount': 50000,
            'currency': 'CLP',
            'due_date': date(2025,12,31),
            'type': '2',
            'department': '3',
            'file': dummy_file
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Budget.objects.count(), 1)
        budget = Budget.objects.first()
        self.assertEqual(budget.upload_folders.count(), 1)
        uploaded_file = budget.upload_folders.first()
        self.assertIn("test_document.pdf", uploaded_file.file.name)

    def test_add_budget_post_multiple_file(self):
        dummy_file_first = SimpleUploadedFile(            
            "doc1.pdf",
            b"dummy file content",
            content_type="application/pdf"
        )
        dummy_file_second = SimpleUploadedFile(            
            "doc2.pdf",
            b"dummy file content",
            content_type="application/pdf"
        )
        data = {
            'title' : 'Title Example',
            'description' : 'Description example lorem ipsum...',  
            'total_mount': 50000,
            'currency': 'EUR',
            'due_date': date(2025,12,31),
            'type': '1',
            'department': '1',
        }
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('app:list_budget'))
        budget = Budget.objects.first()

        BudgetFile.objects.create(budget=budget, file=dummy_file_first)
        BudgetFile.objects.create(budget=budget, file=dummy_file_second)
        self.assertEqual(BudgetFile.objects.count(), 2)
    
    def test_invalid_negative_mount(self):
        data = {
            'title' : 'Title Example',
            'description' : 'Description example lorem ipsum...',  
            'total_mount': -50000,
            'currency': 'EUR',
            'due_date': date(2025,12,31),
            'type': '1',
            'department': '1',
        }

        response = self.client.post(self.url,data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Budget.objects.count(), 0)

    def test_invalid_type_and_department(self):
        data = {
            'title' : 'Title Example',
            'description' : 'Description example lorem ipsum...',  
            'total_mount': 50000,
            'currency': 'EUR',
            'due_date': date(2025,12,31),
            'type': '99999',
            'department': '9999',
        }

        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Budget.objects.count(), 0)

    # Invalid Form Continue


    # BudgetListView