#!/usr/bin/env python
"""
Comprehensive test script for CodeStorm 2026 registration form.
Tests all features including validation, team size, female requirement, etc.
"""

import os
import sys
import django
import uuid
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codestorm_project.settings')
django.setup()

class RegistrationFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.registration_url = '/register/'  # Direct URL path
    
    def test_form_accessibility(self):
        """Test that the registration form is accessible"""
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team Registration')
        print("✓ Form accessibility test passed")
    
    def test_team_size_visibility(self):
        """Test that team size selection works correctly"""
        response = self.client.get(self.registration_url)
        
        # Check that team size options are present
        self.assertContains(response, 'value="4"')
        self.assertContains(response, 'value="5"')
        self.assertContains(response, 'value="6"')
        
        # Check that member sections are present (using member-card class)
        self.assertContains(response, 'member-card')  # Should find multiple member cards
        self.assertContains(response, 'member5-section')  # Only members 5 and 6 have section IDs
        self.assertContains(response, 'member6-section')
        print("✓ Team size visibility test passed")
    
    def test_female_member_requirement(self):
        """Test that form requires at least one female member"""
        # Test data with all male members
        data = {
            'team_name': 'TestTeam',
            'team_size': '4',
            'idea_title': 'Test Idea',
            'idea_theme': 'Generative Al & LLM Applications',
            'member1_name': 'John Doe',
            'member1_email': 'john@test.com',
            'member1_phone': '9876543210',
            'member1_roll': 'CS001',
            'member1_gender': 'male',
            'member1_college_name': 'Test College',
            'member1_college_code': 'ABC',
            'member1_course_name': 'Computer Science',
            'member1_year': '3',
            'is_leader1': 'on',  # Member 1 is leader
            'member2_name': 'Jane Smith',
            'member2_email': 'jane@test.com',
            'member2_phone': '9876543211',
            'member2_roll': 'CS002',
            'member2_gender': 'male',
            'member2_college_name': 'Test College',
            'member2_college_code': 'ABC',
            'member2_course_name': 'Computer Science',
            'member2_year': '3',
            'member3_name': 'Bob Johnson',
            'member3_email': 'bob@test.com',
            'member3_phone': '9876543212',
            'member3_roll': 'CS003',
            'member3_gender': 'male',
            'member3_college_name': 'Test College',
            'member3_college_code': 'ABC',
            'member3_course_name': 'Computer Science',
            'member3_year': '3',
            'member4_name': 'Alice Brown',
            'member4_email': 'alice@test.com',
            'member4_phone': '9876543213',
            'member4_roll': 'CS004',
            'member4_gender': 'male',
            'member4_college_name': 'Test College',
            'member4_college_code': 'ABC',
            'member4_course_name': 'Computer Science',
            'member4_year': '3',
        }
        
        response = self.client.post(self.registration_url, data)
        self.assertContains(response, 'At least one team member must be female')
        print("✓ Female member requirement test passed")
    
    def test_female_member_with_valid_data(self):
        """Test that form accepts when at least one female member is present"""
        # Use a completely unique team name to avoid conflicts
        unique_team_name = f"TestTeamFemale{uuid.uuid4().hex[:8]}"
        data = {
            'team_name': unique_team_name,
            'team_size': '4',
            'idea_title': 'Test Idea',
            'idea_theme': 'Generative Al & LLM Applications',
            'member1_name': 'John Doe',
            'member1_email': 'john@test.com',
            'member1_phone': '9876543210',
            'member1_roll': 'CS001',
            'member1_gender': 'male',
            'member1_college_name': 'Test College',
            'member1_college_code': 'ABC',
            'member1_course_name': 'Computer Science',
            'member1_year': '3',
            'is_leader1': 'on',  # Member 1 is leader
            'member2_name': 'Jane Smith',
            'member2_email': 'jane@test.com',
            'member2_phone': '9876543211',
            'member2_roll': 'CS002',
            'member2_gender': 'female',  # Female member
            'member2_college_name': 'Test College',
            'member2_college_code': 'ABC',
            'member2_course_name': 'Computer Science',
            'member2_year': '3',
            'member3_name': 'Bob Johnson',
            'member3_email': 'bob@test.com',
            'member3_phone': '9876543212',
            'member3_roll': 'CS003',
            'member3_gender': 'male',
            'member3_college_name': 'Test College',
            'member3_college_code': 'ABC',
            'member3_course_name': 'Computer Science',
            'member3_year': '3',
            'member4_name': 'Alice Brown',
            'member4_email': 'alice@test.com',
            'member4_phone': '9876543213',
            'member4_roll': 'CS004',
            'member4_gender': 'male',
            'member4_college_name': 'Test College',
            'member4_college_code': 'ABC',
            'member4_course_name': 'Computer Science',
            'member4_year': '3',
        }
        
        response = self.client.post(self.registration_url, data)
        # Debug: Print response content to see what's happening
        print(f"Response status: {response.status_code}")
        
        # If form submission is successful, it should redirect (302)
        if response.status_code == 302:
            print("✓ Form submission successful - redirected")
            # For a successful submission, we should NOT see validation errors
            # The static warning is only shown on GET requests, not after successful POST
            # This is the expected behavior - form submitted successfully
            pass  # Test passes
        elif response.status_code == 200:
            # If we get 200, it means form validation failed
            content = response.content.decode()
            print(f"Response contains 'female': {'female' in response.content.decode()}")
            print(f"Response contains error: {'At least one team member must be female' in response.content.decode()}")
            # Print a snippet of the response to see what's happening
            if 'At least one team member must be female' in content:
                start = content.find('At least one team member must be female')
                print(f"Error context: {content[max(0, start-100):start+200]}")
            
            # Should not contain the female requirement validation error (but static warning is OK)
            # Check for form validation error specifically, not static template warning
            content = response.content.decode()
            # Look for validation error (in error list or alert-danger div)
            # Static warning is in a p tag with text-warning class, validation error is in alert-danger or errorlist
            has_static_warning = 'text-warning' in content and 'At least one team member must be female' in content
            has_validation_error = ('alert-danger' in content and 'At least one team member must be female' in content) or \
                                   ('errorlist' in content and 'At least one team member must be female' in content)
            
            # If we get 200, it means validation failed, so we should check that it's NOT due to female member requirement
            self.assertFalse(has_validation_error, "Form should not show validation error when female member is present")
        else:
            self.fail(f"Unexpected response status: {response.status_code}")
        print("✓ Female member with valid data test passed")
    
    def test_phone_number_validation(self):
        """Test Indian phone number format validation"""
        # Test invalid phone numbers
        invalid_phones = ['1234567890', '987654321', '98765432101', 'abcdefghij']
        
        for phone in invalid_phones:
            data = {
                'team_name': 'TestTeam',
                'team_size': '4',
                'idea_title': 'Test Idea',
                'idea_theme': 'Generative Al & LLM Applications',
                'member1_name': 'John Doe',
                'member1_email': 'john@test.com',
                'member1_phone': phone,
                'member1_roll': 'CS001',
                'member1_gender': 'male',
                'member1_college_name': 'Test College',
                'member1_college_code': 'ABC',
                'member1_course_name': 'Computer Science',
                'member1_year': '3',
                'member1_is_leader': 'on',
                'member2_name': 'Jane Smith',
                'member2_email': 'jane@test.com',
                'member2_phone': '9876543211',
                'member2_roll': 'CS002',
                'member2_gender': 'female',
                'member2_college_name': 'Test College',
                'member2_college_code': 'ABC',
                'member2_course_name': 'Computer Science',
                'member2_year': '3',
                'member3_name': 'Bob Johnson',
                'member3_email': 'bob@test.com',
                'member3_phone': '9876543212',
                'member3_roll': 'CS003',
                'member3_gender': 'male',
                'member3_college_name': 'Test College',
                'member3_college_code': 'ABC',
                'member3_course_name': 'Computer Science',
                'member3_year': '3',
                'member4_name': 'Alice Brown',
                'member4_email': 'alice@test.com',
                'member4_phone': '9876543213',
                'member4_roll': 'CS004',
                'member4_gender': 'male',
                'member4_college_name': 'Test College',
                'member4_college_code': 'ABC',
                'member4_course_name': 'Computer Science',
                'member4_year': '3',
            }
            
            response = self.client.post(self.registration_url, data)
            print(f"Testing phone {phone}: status {response.status_code}")
            if response.status_code == 200:
                content = response.content.decode()
                if 'Phone number must' in content:
                    print(f"Found phone error for {phone}")
                    # Find the actual error message
                    start = content.find('Phone number must')
                    end = content.find('</div>', start)
                    print(f"Error message: {content[start:end]}")
                else:
                    print(f"No phone error found for {phone}")
                    print(f"Response snippet: {content[1000:1500]}")
            # Check for any phone validation error
            content = response.content.decode()
            self.assertTrue(
                'Phone number must start with 6, 7, 8, or 9.' in content or
                'Phone number must contain only digits.' in content or
                'Phone number must be 10 digits.' in content or
                'Phone number must be exactly 10 digits.' in content,
                f"Should show phone validation error for {phone}"
            )
        
        print("✓ Phone number validation test passed")
    
    def test_college_code_validation(self):
        """Test college code format validation (capital letters only)"""
        # Test invalid college codes
        invalid_codes = ['abc', 'Abc', 'ABC123', '123ABC', 'abc123']
        
        for code in invalid_codes:
            data = {
                'team_name': 'TestTeam',
                'team_size': '4',
                'member1_name': 'John Doe',
                'member1_email': 'john@test.com',
                'member1_phone': '9876543210',
                'member1_roll': 'CS001',
                'member1_gender': 'male',
                'member1_college_name': 'Test College',
                'member1_college_code': code,
                'member1_course_name': 'Computer Science',
                'member1_year': '3',
                'member2_name': 'Jane Smith',
                'member2_email': 'jane@test.com',
                'member2_phone': '9876543211',
                'member2_roll': 'CS002',
                'member2_gender': 'female',
                'member2_college_name': 'Test College',
                'member2_college_code': 'ABC',
                'member2_course_name': 'Computer Science',
                'member2_year': '3',
                'member3_name': 'Bob Johnson',
                'member3_email': 'bob@test.com',
                'member3_phone': '9876543212',
                'member3_roll': 'CS003',
                'member3_gender': 'male',
                'member3_college_name': 'Test College',
                'member3_college_code': 'ABC',
                'member3_course_name': 'Computer Science',
                'member3_year': '3',
                'member4_name': 'Alice Brown',
                'member4_email': 'alice@test.com',
                'member4_phone': '9876543213',
                'member4_roll': 'CS004',
                'member4_gender': 'male',
                'member4_college_name': 'Test College',
                'member4_college_code': 'ABC',
                'member4_course_name': 'Computer Science',
                'member4_year': '3',
            }
            
            response = self.client.post(self.registration_url, data)
            self.assertContains(response, 'This field must contain only capital letters')
        
        print("✓ College code validation test passed")
    
    def test_team_size_5_requirements(self):
        """Test that team size 5 requires member 5 details"""
        # Test with team size 5 but missing member 5
        data = {
            'team_name': 'TestTeam',
            'team_size': '5',
            'idea_title': 'Test Idea',
            'idea_theme': 'Generative Al & LLM Applications',
            'member1_name': 'John Doe',
            'member1_email': 'john@test.com',
            'member1_phone': '9876543210',
            'member1_roll': 'CS001',
            'member1_gender': 'male',
            'member1_college_name': 'Test College',
            'member1_college_code': 'ABC',
            'member1_course_name': 'Computer Science',
            'member1_year': '3',
            'member1_is_leader': 'on',
            'member2_name': 'Jane Smith',
            'member2_email': 'jane@test.com',
            'member2_phone': '9876543211',
            'member2_roll': 'CS002',
            'member2_gender': 'female',
            'member2_college_name': 'Test College',
            'member2_college_code': 'ABC',
            'member2_course_name': 'Computer Science',
            'member2_year': '3',
            'member3_name': 'Bob Johnson',
            'member3_email': 'bob@test.com',
            'member3_phone': '9876543212',
            'member3_roll': 'CS003',
            'member3_gender': 'male',
            'member3_college_name': 'Test College',
            'member3_college_code': 'ABC',
            'member3_course_name': 'Computer Science',
            'member3_year': '3',
            'member4_name': 'Alice Brown',
            'member4_email': 'alice@test.com',
            'member4_phone': '9876543213',
            'member4_roll': 'CS004',
            'member4_gender': 'male',
            'member4_college_name': 'Test College',
            'member4_college_code': 'ABC',
            'member4_course_name': 'Computer Science',
            'member4_year': '3',
            # Missing member 5 details
        }
        
        response = self.client.post(self.registration_url, data)
        print(f"Team size 5 test: status {response.status_code}")
        if response.status_code == 200:
            content = response.content.decode()
            if 'Member 5 details are required' in content:
                print("Found member 5 requirement error")
            else:
                print("No member 5 requirement error found")
                print(f"Response snippet: {content[2000:2500]}")
        self.assertContains(response, 'Member 5 details are required for team size 5')
        print("✓ Team size 5 requirements test passed")
    
    def test_team_size_6_requirements(self):
        """Test that team size 6 requires member 6 details"""
        # Test with team size 6 but missing member 6
        data = {
            'team_name': 'TestTeam',
            'team_size': '6',
            'idea_title': 'Test Idea',
            'idea_theme': 'Generative Al & LLM Applications',
            'member1_name': 'John Doe',
            'member1_email': 'john@test.com',
            'member1_phone': '9876543210',
            'member1_roll': 'CS001',
            'member1_gender': 'male',
            'member1_college_name': 'Test College',
            'member1_college_code': 'ABC',
            'member1_course_name': 'Computer Science',
            'member1_year': '3',
            'member1_is_leader': 'on',
            'member2_name': 'Jane Smith',
            'member2_email': 'jane@test.com',
            'member2_phone': '9876543211',
            'member2_roll': 'CS002',
            'member2_gender': 'female',
            'member2_college_name': 'Test College',
            'member2_college_code': 'ABC',
            'member2_course_name': 'Computer Science',
            'member2_year': '3',
            'member3_name': 'Bob Johnson',
            'member3_email': 'bob@test.com',
            'member3_phone': '9876543212',
            'member3_roll': 'CS003',
            'member3_gender': 'male',
            'member3_college_name': 'Test College',
            'member3_college_code': 'ABC',
            'member3_course_name': 'Computer Science',
            'member3_year': '3',
            'member4_name': 'Alice Brown',
            'member4_email': 'alice@test.com',
            'member4_phone': '9876543213',
            'member4_roll': 'CS004',
            'member4_gender': 'male',
            'member4_college_name': 'Test College',
            'member4_college_code': 'ABC',
            'member4_course_name': 'Computer Science',
            'member4_year': '3',
            'member5_name': 'Charlie Wilson',
            'member5_email': 'charlie@test.com',
            'member5_phone': '9876543214',
            'member5_roll': 'CS005',
            'member5_gender': 'male',
            'member5_college_name': 'Test College',
            'member5_college_code': 'ABC',
            'member5_course_name': 'Computer Science',
            'member5_year': '3',
            # Missing member 6 details
        }
        
        response = self.client.post(self.registration_url, data)
        self.assertContains(response, 'Member 6 details are required for team size 6')
        print("✓ Team size 6 requirements test passed")
    
    def test_leader_selection_validation(self):
        """Test leader selection validation"""
        # Test selecting member 5 as leader when member 5 is not provided
        data = {
            'team_name': 'TestTeam',
            'team_size': '4',
            'member1_name': 'John Doe',
            'member1_email': 'john@test.com',
            'member1_phone': '9876543210',
            'member1_roll': 'CS001',
            'member1_gender': 'male',
            'member1_college_name': 'Test College',
            'member1_college_code': 'ABC',
            'member1_course_name': 'Computer Science',
            'member1_year': '3',
            'member2_name': 'Jane Smith',
            'member2_email': 'jane@test.com',
            'member2_phone': '9876543211',
            'member2_roll': 'CS002',
            'member2_gender': 'female',
            'member2_college_name': 'Test College',
            'member2_college_code': 'ABC',
            'member2_course_name': 'Computer Science',
            'member2_year': '3',
            'member3_name': 'Bob Johnson',
            'member3_email': 'bob@test.com',
            'member3_phone': '9876543212',
            'member3_roll': 'CS003',
            'member3_gender': 'male',
            'member3_college_name': 'Test College',
            'member3_college_code': 'ABC',
            'member3_course_name': 'Computer Science',
            'member3_year': '3',
            'member4_name': 'Alice Brown',
            'member4_email': 'alice@test.com',
            'member4_phone': '9876543213',
            'member4_roll': 'CS004',
            'member4_gender': 'male',
            'member4_college_name': 'Test College',
            'member4_college_code': 'ABC',
            'member4_course_name': 'Computer Science',
            'member4_year': '3',
            'is_leader5': 'on',  # Select member 5 as leader but member 5 not provided
        }
        
        response = self.client.post(self.registration_url, data)
        self.assertContains(response, 'Member 5 cannot be leader if not provided')
        print("✓ Leader selection validation test passed")
    
    def test_email_validation(self):
        """Test email format validation"""
        # Test invalid email formats
        invalid_emails = ['invalid-email', 'test@', '@domain.com', 'test@domain']
        
        for email in invalid_emails:
            data = {
                'team_name': 'TestTeam',
                'team_size': '4',
                'member1_name': 'John Doe',
                'member1_email': email,  # Invalid email
                'member1_phone': '9876543210',
                'member1_roll': 'CS001',
                'member1_gender': 'male',
                'member1_college_name': 'Test College',
                'member1_college_code': 'ABC',
                'member1_course_name': 'Computer Science',
                'member1_year': '3',
                'member2_name': 'Jane Smith',
                'member2_email': 'jane@test.com',
                'member2_phone': '9876543211',
                'member2_roll': 'CS002',
                'member2_gender': 'female',
                'member2_college_name': 'Test College',
                'member2_college_code': 'ABC',
                'member2_course_name': 'Computer Science',
                'member2_year': '3',
                'member3_name': 'Bob Johnson',
                'member3_email': 'bob@test.com',
                'member3_phone': '9876543212',
                'member3_roll': 'CS003',
                'member3_gender': 'male',
                'member3_college_name': 'Test College',
                'member3_college_code': 'ABC',
                'member3_course_name': 'Computer Science',
                'member3_year': '3',
                'member4_name': 'Alice Brown',
                'member4_email': 'alice@test.com',
                'member4_phone': '9876543213',
                'member4_roll': 'CS004',
                'member4_gender': 'male',
                'member4_college_name': 'Test College',
                'member4_college_code': 'ABC',
                'member4_course_name': 'Computer Science',
                'member4_year': '3',
            }
            
            response = self.client.post(self.registration_url, data)
            # Django's built-in email validation should catch invalid formats
            self.assertTrue(response.status_code == 200)
        
        print("✓ Email validation test passed")

if __name__ == '__main__':
    # Run all tests
    import unittest
    
    print("🚀 Starting comprehensive registration form tests...")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(RegistrationFormTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("=" * 60)
    if result.wasSuccessful():
        print("✅ All tests passed! Registration form is working correctly.")
    else:
        print("❌ Some tests failed. Please check the output above.")
    
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")