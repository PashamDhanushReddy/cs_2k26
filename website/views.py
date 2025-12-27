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
    return {
        'apikey': settings.SUPABASE_KEY,
        'Authorization': f'Bearer {settings.SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation'
    }

def upload_ppt_to_supabase(ppt_file, team_name):
    """Upload PPT file to Supabase storage"""
    try:
        # Generate unique filename
        file_extension = ppt_file.name.split('.')[-1]
        unique_filename = f"{team_name.replace(' ', '_')}_{uuid.uuid4()}.{file_extension}"
        file_path = f"ppt_submissions/{unique_filename}"
        
        # Read file content
        file_content = ppt_file.read()
        
        # Ensure proper URL format
        base_url = settings.SUPABASE_URL.rstrip('/')
        if not base_url.startswith('http'):
            base_url = f"https://{base_url}"
            
        # Upload to Supabase storage
        storage_url = f"{base_url}/storage/v1/object/{settings.SUPABASE_BUCKET_NAME}/{file_path}"
        headers = create_supabase_headers()
        headers['Content-Type'] = ppt_file.content_type
        
        print(f"Uploading PPT to: {storage_url}")
        response = requests.post(storage_url, data=file_content, headers=headers)
        print(f"PPT upload response status: {response.status_code}")
        print(f"PPT upload response: {response.text[:200]}")
        
        response.raise_for_status()
        
        return file_path
    except Exception as e:
        print(f"Error uploading PPT: {str(e)}")
        print(f"Response status: {getattr(response, 'status_code', 'N/A')}")
        print(f"Response text: {getattr(response, 'text', 'N/A')[:500]}")
        raise e

def insert_registration_data(data):
    """Insert registration data into Supabase table"""
    try:
        # Ensure proper URL format
        base_url = settings.SUPABASE_URL.rstrip('/')
        if not base_url.startswith('http'):
            base_url = f"https://{base_url}"
            
        table_url = f"{base_url}/rest/v1/codestorm_registrations"
        headers = create_supabase_headers()
        
        print(f"Inserting data to: {table_url}")
        print(f"Data being sent: {json.dumps(data, indent=2)[:500]}...")
        
        response = requests.post(table_url, json=data, headers=headers)
        print(f"Data insert response status: {response.status_code}")
        print(f"Data insert response: {response.text[:200]}")
        
        response.raise_for_status()
        
        return response.json()
    except Exception as e:
        print(f"Error inserting registration data: {str(e)}")
        print(f"Response status: {getattr(response, 'status_code', 'N/A')}")
        print(f"Response text: {getattr(response, 'text', 'N/A')[:500]}")
        raise e

def register_team(request):
    """Handle team registration"""
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Upload PPT first
                ppt_file = request.FILES.get('ppt_file')
                team_name = form.cleaned_data['team_name']
                
                if ppt_file:
                    ppt_path = upload_ppt_to_supabase(ppt_file, team_name)
                else:
                    ppt_path = None
                
                # Prepare data for Supabase
                registration_data = {
                    'team_name': team_name,
                    'college': form.cleaned_data['college'],
                    'team_size': form.cleaned_data['team_size'],
                    'idea_title': form.cleaned_data['idea_title'],
                    'idea_description': form.cleaned_data['idea_description'],
                    'idea_track': form.cleaned_data['idea_track'],
                    'ppt_file_path': ppt_path,
                    'member1_name': form.cleaned_data['member1_name'],
                    'member1_email': form.cleaned_data['member1_email'],
                    'member1_phone': form.cleaned_data['member1_phone'],
                    'member1_branch': form.cleaned_data['member1_branch'],
                    'member1_year': form.cleaned_data['member1_year'],
                    'is_leader1': form.cleaned_data['is_leader1'],
                    'member2_name': form.cleaned_data.get('member2_name'),
                    'member2_email': form.cleaned_data.get('member2_email'),
                    'member2_phone': form.cleaned_data.get('member2_phone'),
                    'member2_branch': form.cleaned_data.get('member2_branch'),
                    'member2_year': form.cleaned_data.get('member2_year'),
                    'is_leader2': form.cleaned_data.get('is_leader2'),
                    'member3_name': form.cleaned_data.get('member3_name'),
                    'member3_email': form.cleaned_data.get('member3_email'),
                    'member3_phone': form.cleaned_data.get('member3_phone'),
                    'member3_branch': form.cleaned_data.get('member3_branch'),
                    'member3_year': form.cleaned_data.get('member3_year'),
                    'is_leader3': form.cleaned_data.get('is_leader3'),
                    'member4_name': form.cleaned_data.get('member4_name'),
                    'member4_email': form.cleaned_data.get('member4_email'),
                    'member4_phone': form.cleaned_data.get('member4_phone'),
                    'member4_branch': form.cleaned_data.get('member4_branch'),
                    'member4_year': form.cleaned_data.get('member4_year'),
                    'is_leader4': form.cleaned_data.get('is_leader4'),
                    'member5_name': form.cleaned_data.get('member5_name'),
                    'member5_email': form.cleaned_data.get('member5_email'),
                    'member5_phone': form.cleaned_data.get('member5_phone'),
                    'member5_branch': form.cleaned_data.get('member5_branch'),
                    'member5_year': form.cleaned_data.get('member5_year'),
                    'is_leader5': form.cleaned_data.get('is_leader5'),
                    'member6_name': form.cleaned_data.get('member6_name'),
                    'member6_email': form.cleaned_data.get('member6_email'),
                    'member6_phone': form.cleaned_data.get('member6_phone'),
                    'member6_branch': form.cleaned_data.get('member6_branch'),
                    'member6_year': form.cleaned_data.get('member6_year'),
                    'is_leader6': form.cleaned_data.get('is_leader6'),
                }
                
                # Insert into Supabase
                insert_registration_data(registration_data)
                
                return redirect('registration_success')
                
            except Exception as e:
                print(f"Registration error: {str(e)}")
                messages.error(request, f'Error submitting registration: {str(e)}')
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