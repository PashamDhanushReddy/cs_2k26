from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import requests
import uuid
import os
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from .forms import TeamRegistrationForm

# Initialize Cloudinary
cloudinary.config( 
  cloud_name = settings.CLOUDINARY_STORAGE['CLOUD_NAME'], 
  api_key = settings.CLOUDINARY_STORAGE['API_KEY'], 
  api_secret = settings.CLOUDINARY_STORAGE['API_SECRET'],
  secure = True
)

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

def upload_ppt_to_cloudinary(ppt_file, team_name):
    """Upload PPT file to Cloudinary"""
    try:
        # Generate a unique public_id
        # Cloudinary handles extensions automatically usually, but we can keep it in the name if we want
        # or just use the team name + uuid
        unique_filename = f"{team_name.replace(' ', '_')}_{uuid.uuid4()}"
        
        print(f"Uploading PPT to Cloudinary: {unique_filename}")
        
        # Upload to Cloudinary
        # resource_type="auto" allows uploading pdf/ppt as raw or auto-detected
        response = cloudinary.uploader.upload(
            ppt_file, 
            public_id=unique_filename,
            folder="ppt_submissions",
            resource_type="auto"
        )
        
        print(f"Cloudinary upload success. URL: {response.get('secure_url')}")
        
        # Return the secure URL
        return response.get('secure_url')
        
    except Exception as e:
        print(f"Error uploading PPT to Cloudinary: {str(e)}")
        return None

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
        form = TeamRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Upload PPT first
                ppt_file = request.FILES.get('ppt_file')
                team_name = form.cleaned_data['team_name']
                
                ppt_path = None
                if ppt_file:
                    ppt_path = upload_ppt_to_cloudinary(ppt_file, team_name)
                    if ppt_path is None:
                        # PPT upload failed
                        messages.warning(request, 'Note: PPT file could not be uploaded to Cloudinary, but your registration will still be saved.')
                
                # Find the team leader to get default values
                leader_data = None
                if form.cleaned_data['is_leader1']:
                    leader_data = {
                        'college_name': form.cleaned_data['college'],  # Team college is leader's college
                        'course_name': form.cleaned_data['member1_course_name'],
                        'year': form.cleaned_data['member1_year']
                    }
                elif form.cleaned_data['is_leader2']:
                    leader_data = {
                        'college_name': form.cleaned_data['member2_college_name'] or form.cleaned_data['college'],
                        'course_name': form.cleaned_data['member2_course_name'],
                        'year': form.cleaned_data['member2_year']
                    }
                elif form.cleaned_data['is_leader3']:
                    leader_data = {
                        'college_name': form.cleaned_data['member3_college_name'] or form.cleaned_data['college'],
                        'course_name': form.cleaned_data['member3_course_name'],
                        'year': form.cleaned_data['member3_year']
                    }
                elif form.cleaned_data['is_leader4']:
                    leader_data = {
                        'college_name': form.cleaned_data['member4_college_name'] or form.cleaned_data['college'],
                        'course_name': form.cleaned_data['member4_course_name'],
                        'year': form.cleaned_data['member4_year']
                    }
                
                # Helper function to get member data with leader defaults
                def get_member_data(member_num, prefix=''):
                    if leader_data:
                        college_key = f'{prefix}member{member_num}_college_name'
                        course_key = f'{prefix}member{member_num}_course_name'
                        year_key = f'{prefix}member{member_num}_year'
                        
                        college_val = form.cleaned_data.get(college_key, '')
                        course_val = form.cleaned_data.get(course_key, '')
                        year_val = form.cleaned_data.get(year_key, '')
                        
                        # For optional members (5 and 6), return None if no data provided
                        if member_num >= 5 and not college_val and not course_val and not year_val:
                            return {
                                f'member{member_num}_college_name': None,
                                f'member{member_num}_course_name': None,
                                f'member{member_num}_year': None
                            }
                        
                        return {
                            f'member{member_num}_college_name': college_val if college_val else leader_data['college_name'],
                            f'member{member_num}_course_name': course_val if course_val else leader_data['course_name'],
                            f'member{member_num}_year': year_val if year_val else leader_data['year']
                        }
                    else:
                        # If no leader found (shouldn't happen), use empty defaults
                        college_val = form.cleaned_data.get(f'{prefix}member{member_num}_college_name', '')
                        course_val = form.cleaned_data.get(f'{prefix}member{member_num}_course_name', '')
                        year_val = form.cleaned_data.get(f'{prefix}member{member_num}_year', '')
                        
                        # For optional members (5 and 6), return None if no data provided
                        if member_num >= 5 and not college_val and not course_val and not year_val:
                            return {
                                f'member{member_num}_college_name': None,
                                f'member{member_num}_course_name': None,
                                f'member{member_num}_year': None
                            }
                        
                        return {
                            f'member{member_num}_college_name': college_val,
                            f'member{member_num}_course_name': course_val,
                            f'member{member_num}_year': year_val
                        }
                
                # Prepare data for Supabase - match your table structure exactly
                registration_data = {
                    'team_name': team_name,
                    'college': form.cleaned_data['college'],
                    'college_code': form.cleaned_data['college_code'],
                    'branch': form.cleaned_data.get('branch', ''),
                    'team_size': form.cleaned_data.get('team_size', ''),
                    'idea_title': form.cleaned_data['idea_title'],
                    'idea_theme': form.cleaned_data['idea_theme'],
                    'ppt_file_path': ppt_path or '',  # Ensure it's not None
                    'youtube_link': form.cleaned_data.get('youtube_link', ''),
                    'member1_name': form.cleaned_data['member1_name'],
                    'member1_email': form.cleaned_data['member1_email'],
                    'member1_phone': form.cleaned_data['member1_phone'],
                    'member1_roll': form.cleaned_data['member1_roll'],
                    'member1_gender': form.cleaned_data['member1_gender'],
                    'member1_college_name': form.cleaned_data['member1_college_name'],
                    'member1_course_name': form.cleaned_data['member1_course_name'],
                    'member1_year': form.cleaned_data['member1_year'],
                    'is_leader1': form.cleaned_data['is_leader1'],
                    'member2_name': form.cleaned_data['member2_name'],
                    'member2_email': form.cleaned_data['member2_email'],
                    'member2_phone': form.cleaned_data['member2_phone'],
                    'member2_roll': form.cleaned_data['member2_roll'],
                    'member2_gender': form.cleaned_data['member2_gender'],
                    **get_member_data(2),  # college_name, course_name, year with leader defaults
                    'is_leader2': form.cleaned_data['is_leader2'],
                    'member3_name': form.cleaned_data['member3_name'],
                    'member3_email': form.cleaned_data['member3_email'],
                    'member3_phone': form.cleaned_data['member3_phone'],
                    'member3_roll': form.cleaned_data['member3_roll'],
                    'member3_gender': form.cleaned_data['member3_gender'],
                    **get_member_data(3),  # college_name, course_name, year with leader defaults
                    'is_leader3': form.cleaned_data['is_leader3'],
                    'member4_name': form.cleaned_data['member4_name'],
                    'member4_email': form.cleaned_data['member4_email'],
                    'member4_phone': form.cleaned_data['member4_phone'],
                    'member4_roll': form.cleaned_data['member4_roll'],
                    'member4_gender': form.cleaned_data['member4_gender'],
                    **get_member_data(4),  # college_name, course_name, year with leader defaults
                    'is_leader4': form.cleaned_data['is_leader4'],
                    'member5_name': form.cleaned_data.get('member5_name') or None,
                    'member5_email': form.cleaned_data.get('member5_email') or None,
                    'member5_phone': form.cleaned_data.get('member5_phone') or None,
                    'member5_roll': form.cleaned_data.get('member5_roll') or None,
                    'member5_gender': form.cleaned_data.get('member5_gender') or None,
                    **get_member_data(5),  # college_name, course_name, year with leader defaults for optional member
                    'is_leader5': form.cleaned_data.get('is_leader5', False),
                    'member6_name': form.cleaned_data.get('member6_name') or None,
                    'member6_email': form.cleaned_data.get('member6_email') or None,
                    'member6_phone': form.cleaned_data.get('member6_phone') or None,
                    'member6_roll': form.cleaned_data.get('member6_roll') or None,
                    'member6_gender': form.cleaned_data.get('member6_gender') or None,
                    **get_member_data(6),  # college_name, course_name, year with leader defaults for optional member
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