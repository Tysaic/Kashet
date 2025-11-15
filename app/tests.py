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


class DepartmentModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name='WOM'
        )
    
    def test_department_creation(self):

        self.assertEqual(Department.objects.all().first().name, 'WOM')
        self.assertIsNotNone(self.department.id)
        self.assertIsInstance(self.department.name, str)
        max_length = self.department._meta.get_field('name').max_length
        self.assertEqual(max_length, 32)
    
    def test_department_str(self):
        expected = "WOM"
        self.assertEqual(str(self.department), expected)
    
    def test_department_unique_creation(self):
        dept_entel = Department.objects.create(name="ENTEL")
        dept_movistar = Department.objects.create(name="MOVISTAR")

        self.assertEqual(Department.objects.count(), 3)
        self.assertNotEqual(dept_entel.id, dept_movistar.id)
    
    def test_department_budgets_relation(self):
        firt_budget = Budget.objects.create(
            title="Budget 1",
            description = "Description 1",
            total_mount = 10000,
            currency="CLP",
            department=self.department,
            due_date = datetime(2025,12,31,0,0,tzinfo=timezone.utc)
        )
        
        second_budget = Budget.objects.create(
            title="Budget 2",
            description = "Description 2",
            total_mount = 20000,
            currency="CLP",
            department=self.department,
            due_date = datetime(2025,12,31,0,0,tzinfo=timezone.utc)
        )

        self.assertEqual(self.department.budgets.count(), 2)
        self.assertIn(firt_budget, self.department.budgets.all())
        self.assertIn(second_budget, self.department.budgets.all())
    
    def test_department_deletion_with_budgets(self):
        budget = Budget.objects.create(
            title="Budget Test",
            description = "Description",
            total_mount = 10000,
            currency="CLP",
            department=self.department,
            due_date = datetime(2025,12,31,0,0,tzinfo=timezone.utc)
        )

        department_id = self.department.id
        self.department.delete()

        budget.refresh_from_db()
        self.assertIsNone(budget.department)
        self.assertEqual(Budget.objects.count(), 1)


class BudgetResume(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('app:resume_budgets')
    
    def test_budget_resume_test(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/budgets/budget.html')

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
        self.assertTemplateUsed(response, 'app/budgets/budget_add.html')
    

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

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BudgetListView(TestCase):

    def setUp(self):

        for dept in ('WOM', 'ENTEL', 'MOVISTAR'):
            Department.objects.create(name=dept)

        self.firt_budget = Budget.objects.create(
            title="Budget 1",
            description = "Description 1",
            total_mount = 10000,
            currency="CLP",
            department=Department.objects.get(id=1),
            due_date = datetime(2025,12,31,0,0,tzinfo=timezone.utc)
        )
        
        self.second_budget = Budget.objects.create(
            title="Budget 2",
            description = "Description 2",
            total_mount = 20000,
            currency="CLP",
            department=Department.objects.get(id=2),
            due_date = datetime(2025,12,31,0,0,tzinfo=timezone.utc)
        )

        self.third_budget = Budget.objects.create(
            title="Budget 3",
            description = "Description 3",
            total_mount = 300000,
            currency="CLP",
            department=Department.objects.get(id=3),
            due_date = datetime(2025,12,31,0,0,tzinfo=timezone.utc)
        )

        self.client = Client()
        self.url = reverse('app:list_budget')

    def test_list_budget_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/budgets/budget_list.html')
    
    def test_list_budget_display_all(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        self.assertIn('budgets', response.context)
        budgets = response.context['budgets']

        self.assertEqual(budgets.count(), 3)

        self.assertIn(self.firt_budget, budgets)
        self.assertIn(self.second_budget, budgets)
        self.assertIn(self.third_budget, budgets)

    def test_list_budget_displays_correct_data(self):

        response = self.client.get(self.url)

        self.assertContains(response, "Budget 1")
        self.assertContains(response, "Budget 2")
        self.assertContains(response, "Budget 3")
        self.assertContains(response, "Description 1")
        self.assertContains(response, "Description 2")
        self.assertContains(response, "Description 3")
    
    def test_list_budget_empty(self):
        Budget.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        budgets = response.context['budgets']
        self.assertEqual(budgets.count(), 0)


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BudgetDetailView(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name="Movistar")

        self.budget = Budget.objects.create(
            identifier = uuid.uuid4(),
            title = "First Budget.",
            description = "Budget Description ...",
            department = self.department,
            total_mount = 150000,
            currency="CLP",
            type="1"
        )

        self.detail_url = reverse("app:detail_budget", kwargs={"identifier": self.budget.identifier})
        self.update_url = reverse("app:update_budget", kwargs={"identifier": self.budget.identifier})

        def test_budget_detail_view_status_and_template(self):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "app/budgets/budget_detail.html")

        def test_budget_detail_view_context(self):
            response = self.client.get(self.detail_url)
            self.assertEqual(response.context["object"], self.budget)
        
        def test_budget_detail_view_content(self):
            response = self.client.get(self.detail_url)
            self.assertContains(response, "First Budget.")
            self.assertContains(response, "Budget Description ...")
            self.assertContains(response, self.department)
            self.assertContains(response, self.total_mount)
            self.assertContains(response, self.currency)

@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BudgetUpdateView(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name="Movistar")

        self.budget = Budget.objects.create(
            identifier = uuid.uuid4(),
            title = "First Budget March.",
            description = "First Budget Description March.",
            department = self.department,
            total_mount = 150000,
            currency="CLP",
            type="1"
        )

        self.file = BudgetFile.objects.create(
            budget=self.budget,
            file=SimpleUploadedFile("budget.pdf", b"Data Dummy.", content_type="application/pdf")
        )

        self.url = reverse("app:update_budget", kwargs={"identifier": self.budget.identifier})

    def test_budget_update_view_get(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/budgets/budget_update.html")
        self.assertIn("file_form", response.context)
        self.assertIn("files", response.context)
        self.assertContains(response, "First Budget March.")
        self.assertContains(response, "First Budget Description March.")
    

    
    def test_budget_update_view_post_valid(self):

        data = {
            "title": "Updated budget.",
            "description": "Updated budget description",
            "department": self.department.id,
            "total_mount": 250000,
            "currency": "USD",
            "type": "1"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        self.budget.refresh_from_db()
        self.assertEqual(self.budget.title, "Updated budget.")
        self.assertEqual(self.budget.description, "Updated budget description")
        self.assertEqual(self.budget.department, self.department)
        self.assertEqual(self.budget.total_mount, 250000)

    
    def test_budget_update_view_upload_file(self):

        new_file = SimpleUploadedFile("New_tax_document.pdf", b"loremp ipsum", content_type="application/pdf")
        response = self.client.post(self.url, {"file": new_file})

        self.assertEqual(response.status_code, 200)

        files = BudgetFile.objects.filter(budget=self.budget)
        self.assertEqual(files.count(), 2)
        self.assertTrue(any("New_tax_document.pdf" in f.file.name for f in files))

    def test_budget_update_view_delete_file(self):

        response = self.client.post(self.url, {"delete_file": self.file.id})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(BudgetFile.objects.filter(id=self.file.id).exists())
    
    def test_budget_update_view_department_and_type(self):
        new_department = Department.objects.create(name="Entel")
        
        data = {
            "title": "Changed budget",
            "description": "Budget with updated department and type",
            "department": new_department.id,
            "total_mount": 350000,
            "currency": "USD",
            "type": "2"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        self.budget.refresh_from_db()
        self.assertEqual(self.budget.department, new_department)
        self.assertEqual(self.budget.type, "2")
        self.assertEqual(self.budget.total_mount, 350000)
        self.assertEqual(self.budget.currency, "USD")
        self.assertEqual(self.budget.title, "Changed budget")
        self.assertEqual(self.budget.description, "Budget with updated department and type")


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BudgetDeleteView(TestCase):

    def setUp(self):
        
        self.department = Department.objects.create(name="WOM")
        self.budget = Budget.objects.create(
            identifier = uuid.uuid4(),
            title = "Budget to delete",
            description = "Description to delete",
            department = self.department,
            total_mount=10000,
            currency="USD",
            type=1
        )

        self.test_file = SimpleUploadedFile("testing_file.pdf", b"Content to testing", content_type="application/pdf")
        self.budget_file = BudgetFile.objects.create(budget=self.budget, file = self.test_file)
        self.file_path = self.budget_file.file.path
        self.folder_path = os.path.dirname(self.file_path)

        self.url = reverse("app:delete_budget", kwargs={'identifier': self.budget.identifier})
    
    def test_budget_delete_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/budgets/budget_delete.html")
        self.assertContains(response, "Eliminar definitivamente")

    
    def test_budget_delete_post(self):
        #existing yet the data before delete?
        self.assertTrue(Budget.objects.filter(id=self.budget.id).exists())
        self.assertTrue(BudgetFile.objects.filter(budget=self.budget).exists())
        self.assertTrue(os.path.isfile(self.file_path))

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Budget.objects.filter(id=self.budget.id).exists())
        self.assertFalse(BudgetFile.objects.filter(budget=self.budget).exists())
        self.assertFalse(os.path.exists(self.file_path))
        self.assertFalse(os.path.exists(self.folder_path))
    
    def test_budget_delete_invalid_identifier(self):
        fake_url = reverse("app:delete_budget", kwargs={'identifier': uuid.uuid4()})
        response = self.client.get(fake_url)
        self.assertEqual(response.status_code, 404)




"""
New testing with new fields of Budget:

* edit

Testing Models:

BILLS
CURRENCY
TYPETRANSACTION
STATUS_TRANSACTION

Views for the above models
BILLS
CURRENCY
TYPETRANSACTION
STATUS_TRANSACTION


FIX Budget with news relationships


* Testear si esta aprobado o denegado (bills y budget) no se puede eliminar
* Si budget tiene bills no se puede eliminar.
"""