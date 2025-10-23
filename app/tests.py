from django.test import TestCase
from datetime import date
from .models import Budget, BudgetFile
from django.core.files.uploadedfile import SimpleUploadedFile
import uuid



class BudgetModelTest(TestCase):

    def setUp(self):
        self.budget = Budget.objects.create(
            name = "Marketing Budget 01 Testing",
            description = "Social media and campaings",
            total_mount = 1500.0,
            currency = "CLP",
            identifier = uuid.uuid4(),
            due_date = date(2026,11,30)
        )
    
    def test_budget_creation(self):
        """Ensure the budget object is created correctly."""
        today = date.today()
        self.assertEqual(self.budget.name, "Marketing Budget 01 Testing")
        self.assertEqual(self.budget.description, "Social media and campaings")
        self.assertEqual(self.budget.total_mount, 1500.0)
        self.assertEqual(self.budget.currency, "CLP")
        self.assertTrue(self.budget.enable)
        self.assertEqual(self.budget.created_at, today)
        self.assertEqual(self.budget.due_date, date(2026,11,30))
        self.assertIsInstance(self.budget.identifier, uuid.UUID)
    
    def test_budget_model_str(self):
        expected = "Marketing Budget 01 Testing - Social media and campaings - (1500.0 CLP)"
        self.assertEqual(str(self.budget), expected)
        
class BudgetFileModelTest(TestCase):

    def setUp(self):
        self.budget = Budget.objects.create(
            name = "File Uploader 1",
            description = "File uploader description 1",
            total_mount = 2000.0,
            currency = "CLP",
            identifier = uuid.uuid4(),
            due_date = date(2026,11,30)
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