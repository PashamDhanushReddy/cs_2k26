from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .supabase_client import get_supabase_client
from django.conf import settings
import base64
import urllib.parse
import csv
import json
from datetime import datetime
import pandas as pd
from io import BytesIO

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'dashboard/login.html')

@login_required(login_url='login')
def update_selection_status_view(request):
    """
    API endpoint to update the selection status of a registration.
    Expects POST request with registration_id and selection_status.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        registration_id = data.get('registration_id')
        selection_status = data.get('selection_status')
        
        # Validate inputs
        if not registration_id or not selection_status:
            return JsonResponse({'error': 'registration_id and selection_status are required'}, status=400)
        
        # Validate selection status value
        valid_statuses = ['pending', 'selected', 'rejected', 'waitlisted']
        if selection_status not in valid_statuses:
            return JsonResponse({'error': f'Invalid selection_status. Must be one of: {", ".join(valid_statuses)}'}, status=400)
        
        # Update in Supabase
        supabase = get_supabase_client()
        response = supabase.table('codestorm_registrations').update({
            'selection_status': selection_status
        }).eq('id', registration_id).execute()
        
        if response.data:
            return JsonResponse({
                'success': True,
                'message': 'Selection status updated successfully',
                'registration_id': registration_id,
                'new_status': selection_status
            })
        else:
            return JsonResponse({'error': 'Failed to update selection status'}, status=500)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def debug_storage_view(request):
    """Debug view to show what's in the Supabase storage bucket"""
    supabase = get_supabase_client()
    
    context = {
        'bucket_name': settings.SUPABASE_BUCKET_NAME,
        'files': [],
        'error': None
    }
    
    try:
        # List files in the bucket
        files_response = supabase.storage.from_(settings.SUPABASE_BUCKET_NAME).list()
        context['files'] = files_response if files_response else []
        
        # Also try to get public URLs for files
        for file in context['files']:
            file_name = file.get('name', '')
            if file_name:
                try:
                    # Try to get public URL (if bucket is public)
                    public_url = supabase.storage.from_(settings.SUPABASE_BUCKET_NAME).get_public_url(file_name)
                    file['public_url'] = public_url
                except:
                    file['public_url'] = None
                    
    except Exception as e:
        context['error'] = str(e)
    
    return render(request, 'dashboard/debug_storage.html', context)

@login_required(login_url='login')
def debug_fields_view(request):
    """Debug view to show actual database field names"""
    supabase = get_supabase_client()
    
    # Fetch just one registration to see field names
    response = supabase.table('codestorm_registrations').select("*").limit(1).execute()
    registration = response.data[0] if response.data else None
    
    context = {
        'registration': registration,
        'fields': list(registration.keys()) if registration else [],
        'sample_data': registration if registration else {}
    }
    
    return render(request, 'dashboard/debug_fields.html', context)

@login_required(login_url='login')
def dashboard_view(request):
    supabase = get_supabase_client()
    
    # Get filter parameters from request
    college_code_filter = request.GET.get('college_code', '')
    team_size_filter = request.GET.get('team_size', '')
    has_ppt_filter = request.GET.get('has_ppt', '')
    date_filter = request.GET.get('date', '')
    idea_theme_filter = request.GET.get('idea_theme', '')
    selection_status_filter = request.GET.get('selection_status', '')
    
    # Build query
    query = supabase.table('codestorm_registrations').select("*")
    
    # Apply filters
    if college_code_filter:
        query = query.ilike('college_code', f'%{college_code_filter}%')
    # Note: Team size filter will be applied after data processing since it's calculated dynamically
    
    # Apply idea theme filter
    if idea_theme_filter:
        query = query.ilike('idea_theme', f'%{idea_theme_filter}%')
    
    # Apply selection status filter
    if selection_status_filter:
        query = query.eq('selection_status', selection_status_filter)
    
    # Apply date filter
    if date_filter:
        try:
            # Parse the date and convert to ISO format for Supabase
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
            # Filter for the entire day (from 00:00:00 to 23:59:59)
            start_datetime = filter_date.replace(hour=0, minute=0, second=0)
            end_datetime = filter_date.replace(hour=23, minute=59, second=59)
            query = query.gte('registration_date', start_datetime.isoformat()).lte('registration_date', end_datetime.isoformat())
        except ValueError:
            pass  # Invalid date format, ignore filter
    
    # Execute query
    response = query.execute()
    registrations = response.data
    
    # Debug: Print available fields from first registration
    if registrations:
        print("=== DATABASE FIELD ANALYSIS ===")
        print("Available fields in registration:")
        for key, value in registrations[0].items():
            print(f"  {key}: {type(value).__name__}")
            if 'date' in key.lower() or 'time' in key.lower():
                print(f"    -> DATE/TIME FIELD FOUND: {key} = {value}")
        print(f"Total registrations: {len(registrations)}")
        print("=== END FIELD ANALYSIS ===")
    else:
        print("No registrations found")
    
    # Get all unique values for filter dropdowns from unfiltered data
    # First, get all registrations without filters to populate dropdowns
    all_query = supabase.table('codestorm_registrations').select("*")
    all_response = all_query.execute()
    all_registrations = all_response.data
    
    # Process all registrations to get unique dropdown values
    all_processed = []
    for reg in all_registrations:
        # Count team members (excluding empty ones)
        team_size = 0
        for i in range(1, 7):
            member_name = reg.get(f'member{i}_name')
            if member_name:
                team_size += 1
        
        all_processed.append({
            'college_code': reg.get('college_code', 'N/A'),
            'team_size': team_size,
            'idea_theme': reg.get('idea_theme', 'N/A'),
        })
    
    # Get unique values for dropdowns from all data
    all_college_codes = sorted(set(reg['college_code'] for reg in all_processed if reg['college_code'] != 'N/A'))
    
    # Team sizes should show all possible options (4, 5, 6 members)
    all_team_sizes = ['4', '5', '6']
    
    # Get all unique themes from the database, plus add any missing standard themes
    db_themes = sorted(set(reg['idea_theme'] for reg in all_processed if reg['idea_theme'] != 'N/A'))
    
    # Add any missing standard themes that should always be available
    standard_themes = [
        'Artificial Intelligence & Machine Learning',
        'Web Development',
        'Mobile App Development', 
        'Blockchain & Cryptocurrency',
        'Internet of Things (IoT)',
        'Cybersecurity',
        'Data Science & Analytics',
        'Cloud Computing',
        'Game Development',
        'Fintech',
        'Health Tech',
        'Ed Tech',
        'E-commerce',
        'Social Impact',
        'Environment & Sustainability',
        'Robotics',
        'Augmented Reality & Virtual Reality'
    ]
    
    # Combine database themes with standard themes and remove duplicates
    all_idea_themes = sorted(set(db_themes + standard_themes))
    
    # Process registrations to generate download links and essential data
    processed_registrations = []
    for reg in registrations:
        # Use the correct field name: ppt_file_path
        ppt_path = reg.get('ppt_file_path')
        has_ppt = bool(ppt_path)
        
        # Apply PPT filter if specified
        if has_ppt_filter == 'yes' and not has_ppt:
            continue
        if has_ppt_filter == 'no' and has_ppt:
            continue
        
        # Find team leader
        team_leader_name = None
        team_leader_email = None
        team_leader_phone = None
        
        # Check each member to find the leader
        for i in range(1, 7):
            if reg.get(f'is_leader{i}'):
                team_leader_name = reg.get(f'member{i}_name')
                team_leader_email = reg.get(f'member{i}_email')
                team_leader_phone = reg.get(f'member{i}_phone')
                break
        
        # Count team members (excluding empty ones)
        team_size = 0
        team_members = []
        for i in range(1, 7):
            member_name = reg.get(f'member{i}_name')
            member_email = reg.get(f'member{i}_email')
            member_phone = reg.get(f'member{i}_phone')
            member_roll = reg.get(f'member{i}_roll')
            is_leader = reg.get(f'is_leader{i}', False)
            
            if member_name:
                team_size += 1
                team_members.append({
                    'name': member_name,
                    'email': member_email,
                    'phone': member_phone,
                    'roll': member_roll,
                    'is_leader': is_leader
                })
        
        # Apply team size filter if specified
        if team_size_filter and str(team_size) != team_size_filter:
            continue
        
        # Parse registration date
        registration_date = reg.get('registration_date', 'N/A')
        if registration_date != 'N/A' and registration_date:
            try:
                # Parse the ISO format date string
                registration_date = datetime.fromisoformat(registration_date.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                registration_date = 'N/A'
        
        # Create essential admin data structure
        essential_data = {
            'id': reg.get('id'),
            'team_name': reg.get('team_name', 'N/A'),
            'team_leader_name': team_leader_name or 'N/A',
            'team_leader_email': team_leader_email or 'N/A',
            'team_leader_phone': team_leader_phone or 'N/A',
            'college_name': reg.get('college', 'N/A'),
            'college_code': reg.get('college_code', 'N/A'),
            'team_size': team_size,
            'registration_date': registration_date,
            'has_ppt': has_ppt,
            'idea_title': reg.get('idea_title', 'N/A'),
            'idea_theme': reg.get('idea_theme', 'N/A'),
            'youtube_link': reg.get('youtube_link', 'N/A'),
            'ppt_file_path': reg.get('ppt_file_path', ''),  # Add Google Drive link
            'selection_status': reg.get('selection_status', 'pending'),
        }
        
        essential_data['team_members'] = team_members
        essential_data['team_members_json'] = json.dumps(team_members)
        
        # Process PPT download links
        if ppt_path:
            # Check if it's a Cloudinary URL (or any full URL)
            if ppt_path.startswith('http'):
                essential_data['download_url'] = ppt_path
                essential_data['download_filename'] = ppt_path.split('/')[-1]
            else:
                try:
                    # Generate a signed URL valid for 1 hour (3600 seconds)
                    res = supabase.storage.from_(settings.SUPABASE_BUCKET_NAME).create_signed_url(ppt_path, 3600)
                    if res and 'signedURL' in res:
                        essential_data['download_url'] = res['signedURL']
                        essential_data['download_path'] = base64.b64encode(ppt_path.encode()).decode()
                        essential_data['download_filename'] = ppt_path.split('/')[-1]
                    else:
                        essential_data['download_error'] = "No signed URL generated"
                except Exception as e:
                    essential_data['download_error'] = str(e)
        else:
            essential_data['download_error'] = "No PPT file uploaded"
            
        processed_registrations.append(essential_data)
    
    # Get total count of all registrations from database (unfiltered)
    total_registrations = len(all_registrations) if all_registrations else 0
    
    context = {
        'registrations': processed_registrations,
        'filters': {
            'college_code': college_code_filter,
            'team_size': team_size_filter,
            'has_ppt': has_ppt_filter,
            'date': date_filter,
            'idea_theme': idea_theme_filter,
            'selection_status': selection_status_filter,
        },
        'college_codes': all_college_codes,
        'team_sizes': all_team_sizes,
        'idea_themes': all_idea_themes,
        'total_registrations': total_registrations,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url='login')
def download_ppt_view(request, ppt_path):
    supabase = get_supabase_client()
    try:
        # Generate a short-lived signed URL (60 seconds)
        res = supabase.storage.from_(settings.SUPABASE_BUCKET_NAME).create_signed_url(ppt_path, 60)
        if res and 'signedURL' in res:
            return redirect(res['signedURL'])
    except Exception:
        pass
    return HttpResponse("File not found or error generating link", status=404)

@login_required(login_url='login')
def export_registrations_view(request):
    supabase = get_supabase_client()
    
    # Get filter parameters
    college_code_filter = request.GET.get('college_code', '')
    team_size_filter = request.GET.get('team_size', '')
    has_ppt_filter = request.GET.get('has_ppt', '')
    date_filter = request.GET.get('date', '')
    idea_theme_filter = request.GET.get('idea_theme', '')
    selection_status_filter = request.GET.get('selection_status', '')
    
    # Build query
    query = supabase.table('codestorm_registrations').select("*")
    
    if college_code_filter:
        query = query.ilike('college_code', f'%{college_code_filter}%')
    
    if idea_theme_filter:
        query = query.ilike('idea_theme', f'%{idea_theme_filter}%')
        
    if selection_status_filter:
        query = query.eq('selection_status', selection_status_filter)
        
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d')
            start_datetime = filter_date.replace(hour=0, minute=0, second=0)
            end_datetime = filter_date.replace(hour=23, minute=59, second=59)
            query = query.gte('registration_date', start_datetime.isoformat()).lte('registration_date', end_datetime.isoformat())
        except ValueError:
            pass

    response = query.execute()
    registrations = response.data
    
    # Process data
    processed_data = []
    for reg in registrations:
        ppt_path = reg.get('ppt_file_path')
        has_ppt = bool(ppt_path)
        
        if has_ppt_filter == 'yes' and not has_ppt:
            continue
        if has_ppt_filter == 'no' and has_ppt:
            continue
            
        # Find leader and collect detailed member information
        team_leader_name = 'N/A'
        team_leader_email = 'N/A'
        team_leader_phone = 'N/A'
        
        # Calculate team size and members string
        team_size = 0
        members_list = []
        detailed_members = []  # Store detailed member info for export
        
        for i in range(1, 7):
            name = reg.get(f'member{i}_name')
            email = reg.get(f'member{i}_email')
            phone = reg.get(f'member{i}_phone')
            roll = reg.get(f'member{i}_roll')
            is_leader = reg.get(f'is_leader{i}')
            
            if name:
                team_size += 1
                member_str = f"{name} ({roll})"
                if is_leader:
                    team_leader_name = name
                    team_leader_email = email
                    team_leader_phone = phone
                    member_str += " [LEADER]"
                members_list.append(member_str)
                
                # Store detailed member info
                detailed_members.append({
                    'name': name,
                    'email': email or 'N/A',
                    'phone': phone or 'N/A',
                    'roll': roll or 'N/A',
                    'is_leader': is_leader
                })
        
        if team_size_filter and str(team_size) != team_size_filter:
            continue
            
        processed_data.append({
            'Team Name': reg.get('team_name', 'N/A'),
            'Team Leader': team_leader_name,
            'Leader Email': team_leader_email,
            'Leader Phone': team_leader_phone,
            'College': reg.get('college', 'N/A'),
            'College Code': reg.get('college_code', 'N/A'),
            'Team Size': team_size,
            'Selection Status': reg.get('selection_status', 'pending'),
            'Team Members': "; ".join(members_list),
            'Registration Date': reg.get('registration_date', 'N/A'),
            'Idea Theme': reg.get('idea_theme', 'N/A'),
            'Idea Title': reg.get('idea_title', 'N/A'),
            'YouTube Link': reg.get('youtube_link', 'N/A'),
            'Detailed Members': detailed_members,  # Store detailed member info for modal
        })

    # Check export format
    export_format = request.GET.get('format', 'csv')
    
    if export_format == 'excel':
        # Create detailed DataFrame with individual member columns
        detailed_data = []
        for reg in processed_data:
            base_row = {
                'Team Name': reg['Team Name'],
                'Team Leader': reg['Team Leader'],
                'Leader Email': reg['Leader Email'],
                'Leader Phone': reg['Leader Phone'],
                'College': reg['College'],
                'College Code': reg['College Code'],
                'Team Size': reg['Team Size'],
                'Selection Status': reg['Selection Status'],
                'Registration Date': reg['Registration Date'],
                'Idea Theme': reg['Idea Theme'],
                'Idea Title': reg['Idea Title'],
                'YouTube Link': reg['YouTube Link'],
            }
            
            # Add individual member details
            if reg.get('Detailed Members'):
                for i, member in enumerate(reg['Detailed Members'], 1):
                    base_row[f'Member {i} Name'] = member['name']
                    base_row[f'Member {i} Roll No'] = member['roll']
                    base_row[f'Member {i} Email'] = member['email']
                    base_row[f'Member {i} Phone'] = member['phone']
                    base_row[f'Member {i} Role'] = 'Team Leader' if member['is_leader'] else 'Member'
            
            detailed_data.append(base_row)
        
        # Create DataFrame
        df = pd.DataFrame(detailed_data)
        
        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Detailed Registrations')
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Detailed Registrations']
            for column_cells in worksheet.columns:
                length = max(len(str(cell.value)) for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(length + 2, 50)  # Cap at 50 chars
        
        output.seek(0)
        
        # Return Excel response
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="codestorm_registrations_detailed.xlsx"'
        return response
    
    # Default to CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="codestorm_registrations_detailed.csv"'

    # Create detailed CSV with individual member columns
    detailed_data = []
    for reg in processed_data:
        base_row = {
            'Team Name': reg['Team Name'],
            'Team Leader': reg['Team Leader'],
            'Leader Email': reg['Leader Email'],
            'Leader Phone': reg['Leader Phone'],
            'College': reg['College'],
            'College Code': reg['College Code'],
            'Team Size': reg['Team Size'],
            'Selection Status': reg['Selection Status'],
            'Registration Date': reg['Registration Date'],
            'Idea Theme': reg['Idea Theme'],
            'Idea Title': reg['Idea Title'],
            'YouTube Link': reg['YouTube Link'],
        }
        
        # Add individual member details
        if reg.get('Detailed Members'):
            for i, member in enumerate(reg['Detailed Members'], 1):
                base_row[f'Member {i} Name'] = member['name']
                base_row[f'Member {i} Roll No'] = member['roll']
                base_row[f'Member {i} Email'] = member['email']
                base_row[f'Member {i} Phone'] = member['phone']
                base_row[f'Member {i} Role'] = 'Team Leader' if member['is_leader'] else 'Member'
        
        detailed_data.append(base_row)

    # Get all fieldnames from the first row (all possible columns)
    fieldnames = list(detailed_data[0].keys()) if detailed_data else []

    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for row in detailed_data:
        writer.writerow(row)
        
    return response
