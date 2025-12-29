#!/usr/bin/env python
"""Debug script to test female member validation with valid data"""

import os
import django
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codestorm_project.settings')
django.setup()

from website.forms import TeamRegistrationForm

def test_female_validation_valid():
    print("Testing female member validation with valid data...")
    
    # Test with female member (should pass)
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
        'member1_is_leader': 'on',
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
    
    form = TeamRegistrationForm(data=data)
    print(f"Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print("Form errors:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        
        print("Non-field errors:")
        for error in form.non_field_errors():
            print(f"  {error}")
    else:
        print("✓ Form validation passed!")

if __name__ == '__main__':
    test_female_validation_valid()