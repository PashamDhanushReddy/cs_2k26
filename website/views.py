from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import requests
import uuid
import os
import json
from .forms import TeamRegistrationForm

def create_supabase_headers():
    """Create headers for Supabase API requests"""
    print(f"=== AUTH DEBUG ===")
    print(f"SUPABASE_KEY from settings: {settings.SUPABASE_KEY[:20]}...")
    print(f"SUPABASE_URL from settings: {settings.SUPABASE_URL}")
    print(f"SUPABASE_KEY length: {len(settings.SUPABASE_KEY) if settings.SUPABASE_KEY else 'None'}")
    print(f"==================")
    
    return {
        'apikey': settings.SUPABASE_KEY,
        'Authorization': f'Bearer {settings.SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

# Note: PPT upload functionality has been removed - now using Google Drive links

def insert_registration_data(data):
    """Insert registration data into Supabase table"""
    response = None
    try:
        # Ensure proper URL format
        base_url = settings.SUPABASE_URL.rstrip('/')
        if not base_url.startswith('http'):
            base_url = f"https://{base_url}"
            
        table_url = f"{base_url}/rest/v1/codestorm_registrations"
        headers = create_supabase_headers()
        
        print(f"=== SUPABASE REQUEST DEBUG ===")
        print(f"URL: {table_url}")
        print(f"Headers: {json.dumps(headers, indent=2)}")
        print(f"Data: {json.dumps(data, indent=2)}")
        print(f"SUPABASE_KEY from settings: {settings.SUPABASE_KEY[:20]}...")
        print(f"==============================")
        
        print(f"Inserting data to: {table_url}")
        print(f"Data being sent: {json.dumps(data, indent=2)[:500]}...")
        
        response = requests.post(table_url, json=data, headers=headers)
        print(f"Data insert response status: {response.status_code}")
        print(f"Data insert response: {response.text[:200]}")
        
        if response.status_code == 409:
            print(f"❌ CONFLICT ERROR: {response.text}")
            print(f"Data being inserted: {json.dumps(data, indent=2)}")
            raise Exception(f"Registration conflict: {response.text}")
        
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"Error inserting registration data: {str(e)}")
        if response:
            print(f"Response status: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
        else:
            print("No response available (error occurred before request)")
        raise e

def register_team(request):
    """Handle team registration"""
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST)
        if form.is_valid():
            try:
                # Get Google Drive link directly from form
                ppt_drive_link = form.cleaned_data['ppt_file_path']
                
                # Prepare data for Supabase - match your table structure exactly
                registration_data = {
                    'team_name': form.cleaned_data['team_name'],
                    'college': form.cleaned_data['college'],
                    'college_code': form.cleaned_data['college_code'],
                    'branch': form.cleaned_data.get('branch', ''),
                    'year_of_study': form.cleaned_data.get('year_of_study', ''),
                    'idea_title': form.cleaned_data['idea_title'],
                    'idea_theme': form.cleaned_data['idea_theme'],
                    'ppt_file_path': ppt_drive_link,  # Store Google Drive link directly
                    'youtube_link': form.cleaned_data.get('youtube_link', ''),
                    'member1_name': form.cleaned_data['member1_name'],
                    'member1_email': form.cleaned_data['member1_email'],
                    'member1_phone': form.cleaned_data['member1_phone'],
                    'member1_roll': form.cleaned_data['member1_roll'],
                    'is_leader1': form.cleaned_data['is_leader1'],
                    'member2_name': form.cleaned_data['member2_name'],
                    'member2_email': form.cleaned_data['member2_email'],
                    'member2_phone': form.cleaned_data['member2_phone'],
                    'member2_roll': form.cleaned_data['member2_roll'],
                    'is_leader2': form.cleaned_data['is_leader2'],
                    'member3_name': form.cleaned_data['member3_name'],
                    'member3_email': form.cleaned_data['member3_email'],
                    'member3_phone': form.cleaned_data['member3_phone'],
                    'member3_roll': form.cleaned_data['member3_roll'],
                    'is_leader3': form.cleaned_data['is_leader3'],
                    'member4_name': form.cleaned_data['member4_name'],
                    'member4_email': form.cleaned_data['member4_email'],
                    'member4_phone': form.cleaned_data['member4_phone'],
                    'member4_roll': form.cleaned_data['member4_roll'],
                    'is_leader4': form.cleaned_data['is_leader4'],
                    'member5_name': form.cleaned_data.get('member5_name', ''),
                    'member5_email': form.cleaned_data.get('member5_email', ''),
                    'member5_phone': form.cleaned_data.get('member5_phone', ''),
                    'member5_roll': form.cleaned_data.get('member5_roll', ''),
                    'is_leader5': form.cleaned_data.get('is_leader5', False),
                    'member6_name': form.cleaned_data.get('member6_name', ''),
                    'member6_email': form.cleaned_data.get('member6_email', ''),
                    'member6_phone': form.cleaned_data.get('member6_phone', ''),
                    'member6_roll': form.cleaned_data.get('member6_roll', ''),
                    'is_leader6': form.cleaned_data.get('is_leader6', False),
                }
                
                # Insert into Supabase
                insert_registration_data(registration_data)
                
                return redirect('registration_success')
                
            except Exception as e:
                error_msg = str(e)
                print(f"Registration error: {error_msg}")
                
                # Handle specific CSRF errors
                if 'CSRF' in error_msg.upper():
                    messages.error(request, 'CSRF verification failed. Please refresh the page and try again.')
                elif 'cannot access local variable' in error_msg:
                    messages.error(request, 'Server configuration error. Please try again or contact support.')
                else:
                    messages.error(request, f'Error submitting registration: {error_msg}')
                
                # If PPT upload failed, we don't need to clean up since we didn't insert data
                
    else:
        form = TeamRegistrationForm()
    
    return render(request, 'website/register.html', {'form': form})

def registration_success(request):
    """Show success page after registration"""
    return render(request, 'website/registration_success.html')

def home(request):
    """Home page view"""
    return render(request, 'website/home.html')