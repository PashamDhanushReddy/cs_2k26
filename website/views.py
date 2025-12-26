from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
import requests
import uuid
from datetime import datetime
from .config import (
    SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_KEY,
    STORAGE_BUCKET_NAME, MAX_FILE_SIZE, ALLOWED_FILE_TYPES,
    VALIDATION_MESSAGES
)

def home(request):
    return render(request, 'website/home.html')

def register(request):
    return render(request, 'website/register.html')

@csrf_exempt
@require_http_methods(["POST"])
def upload_ppt(request):
    """Get signed URL for PPT upload to Supabase Storage"""
    try:
        data = json.loads(request.body)
        file_name = data.get('file_name')
        file_type = data.get('file_type')
        
        if not file_name or not file_type:
            return JsonResponse({'error': VALIDATION_MESSAGES['REQUIRED_FIELD']}, status=400)
        
        if file_type not in ALLOWED_FILE_TYPES:
            return JsonResponse({'error': VALIDATION_MESSAGES['INVALID_FILE_TYPE']}, status=400)
        
        # Generate unique file name
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        clean_file_name = file_name.replace(' ', '_')
        final_file_name = f"{timestamp}_{unique_id}_{clean_file_name}"
        
        # Generate signed URL for upload (using Supabase Storage API)
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{STORAGE_BUCKET_NAME}/{final_file_name}"
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{STORAGE_BUCKET_NAME}/{final_file_name}"
        
        return JsonResponse({
            'upload_url': upload_url,
            'public_url': public_url,
            'file_name': final_file_name
        })
        
    except Exception as e:
        return JsonResponse({'error': f"{VALIDATION_MESSAGES['UPLOAD_FAILED']} {str(e)}"}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def submit_registration(request):
    """Submit registration data to Supabase"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = [
            'team_name', 'college', 'idea_title', 'idea_theme', 'ppt_file_path',
            'member1_name', 'member1_email', 'member1_phone', 'member1_roll',
            'member2_name', 'member2_email', 'member2_phone', 'member2_roll',
            'member3_name', 'member3_email', 'member3_phone', 'member3_roll',
            'member4_name', 'member4_email', 'member4_phone', 'member4_roll',
            'team_leader'
        ]
        
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f"{VALIDATION_MESSAGES['REQUIRED_FIELD']}: {field}"}, status=400)
        
        # Validate email format
        email_fields = ['member1_email', 'member2_email', 'member3_email', 'member4_email']
        for field in email_fields:
            if data.get(field) and '@' not in data.get(field, ''):
                return JsonResponse({'error': f"{VALIDATION_MESSAGES['INVALID_EMAIL']} for {field}"}, status=400)
        
        # Validate phone numbers (basic validation)
        phone_fields = ['member1_phone', 'member2_phone', 'member3_phone', 'member4_phone']
        for field in phone_fields:
            phone = data.get(field, '')
            if phone and (len(phone) < 10 or not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit()):
                return JsonResponse({'error': f"{VALIDATION_MESSAGES['INVALID_PHONE']} for {field}"}, status=400)
        
        # Prepare data for Supabase
        registration_data = {
            'team_name': data['team_name'].strip(),
            'college': data['college'].strip(),
            'branch': data.get('branch', '').strip(),
            'year_of_study': data.get('year_of_study', '').strip(),
            'idea_title': data['idea_title'].strip(),
            'idea_theme': data['idea_theme'].strip(),
            'ppt_file_path': data['ppt_file_path'].strip(),
            'youtube_link': data.get('youtube_link', '').strip(),
            'member1_name': data['member1_name'].strip(),
            'member1_email': data['member1_email'].strip().lower(),
            'member1_phone': data['member1_phone'].strip(),
            'member1_roll': data['member1_roll'].strip(),
            'is_leader1': data['team_leader'] == '1',
            'member2_name': data['member2_name'].strip(),
            'member2_email': data['member2_email'].strip().lower(),
            'member2_phone': data['member2_phone'].strip(),
            'member2_roll': data['member2_roll'].strip(),
            'is_leader2': data['team_leader'] == '2',
            'member3_name': data['member3_name'].strip(),
            'member3_email': data['member3_email'].strip().lower(),
            'member3_phone': data['member3_phone'].strip(),
            'member3_roll': data['member3_roll'].strip(),
            'is_leader3': data['team_leader'] == '3',
            'member4_name': data['member4_name'].strip(),
            'member4_email': data['member4_email'].strip().lower(),
            'member4_phone': data['member4_phone'].strip(),
            'member4_roll': data['member4_roll'].strip(),
            'is_leader4': data['team_leader'] == '4',
            'member5_name': data.get('member5_name', '').strip(),
            'member5_email': data.get('member5_email', '').strip().lower(),
            'member5_phone': data.get('member5_phone', '').strip(),
            'member5_roll': data.get('member5_roll', '').strip(),
            'is_leader5': data['team_leader'] == '5',
            'member6_name': data.get('member6_name', '').strip(),
            'member6_email': data.get('member6_email', '').strip().lower(),
            'member6_phone': data.get('member6_phone', '').strip(),
            'member6_roll': data.get('member6_roll', '').strip(),
            'is_leader6': data['team_leader'] == '6',
        }
        
        # Insert into Supabase
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/codestorm_registrations",
            headers={
                'apikey': SUPABASE_SERVICE_KEY,
                'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            },
            json=registration_data
        )
        
        if response.status_code in [200, 201]:
            return JsonResponse({
                'success': True, 
                'message': 'Registration successful! Your team has been registered for CodeStorm 2026.'
            })
        else:
            error_msg = f"Supabase error: {response.status_code}"
            try:
                error_detail = response.json()
                if 'message' in error_detail:
                    error_msg += f" - {error_detail['message']}"
            except:
                error_msg += f" - {response.text}"
            
            return JsonResponse({'error': error_msg}, status=response.status_code)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f"{VALIDATION_MESSAGES['REGISTRATION_FAILED']} {str(e)}"}, status=500)
