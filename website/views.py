from django.shortcuts import render
import os
import psycopg2
from psycopg2 import IntegrityError
import uuid

def home(request):
    return render(request, 'website/home.html')

def idea_register(request):
    if request.method == 'POST':
        form_data = request.POST
        errors = []
        
        team_name = form_data.get('team_name', '').strip()
        college = form_data.get('college', '').strip()
        branch = form_data.get('branch', '').strip()
        year_of_study = form_data.get('year_of_study', '').strip()
        idea_title = form_data.get('idea_title', '').strip()
        idea_theme = form_data.get('idea_theme', '').strip()
        youtube_link = form_data.get('youtube_link', '').strip() or None
        
        # Handle file upload
        ppt_upload_url = None
        if 'ppt_file' in request.FILES:
            uploaded_file = request.FILES['ppt_file']
            
            # Validate file size (max 10MB)
            if uploaded_file.size > 10 * 1024 * 1024:
                errors.append('PPT file size must not exceed 10MB.')
            else:
                # For now, we'll store the file locally and create a local URL
                # In production, you'd upload to S3 or similar service
                upload_dir = os.path.join('media', 'codestorm_ppts')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate unique filename
                file_extension = os.path.splitext(uploaded_file.name)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)
                
                try:
                    with open(file_path, 'wb+') as destination:
                        for chunk in uploaded_file.chunks():
                            destination.write(chunk)
                    
                    # Create URL for the uploaded file
                    ppt_upload_url = f"/media/codestorm_ppts/{unique_filename}"
                    
                except Exception as e:
                    errors.append(f'Error uploading PPT file: {str(e)}')
        else:
            errors.append('PPT file upload is required.')
        
        # Member details
        member1_name = form_data.get('member1_name', '').strip()
        member1_email = form_data.get('member1_email', '').strip()
        member1_phone = form_data.get('member1_phone', '').strip()
        member1_roll = form_data.get('member1_roll', '').strip()
        
        member2_name = form_data.get('member2_name', '').strip()
        member2_email = form_data.get('member2_email', '').strip()
        member2_phone = form_data.get('member2_phone', '').strip()
        member2_roll = form_data.get('member2_roll', '').strip()
        
        member3_name = form_data.get('member3_name', '').strip()
        member3_email = form_data.get('member3_email', '').strip()
        member3_phone = form_data.get('member3_phone', '').strip()
        member3_roll = form_data.get('member3_roll', '').strip()
        
        member4_name = form_data.get('member4_name', '').strip()
        member4_email = form_data.get('member4_email', '').strip()
        member4_phone = form_data.get('member4_phone', '').strip()
        member4_roll = form_data.get('member4_roll', '').strip()
        
        member5_name = form_data.get('member5_name', '').strip() or None
        member5_email = form_data.get('member5_email', '').strip() or None
        member5_phone = form_data.get('member5_phone', '').strip() or None
        member5_roll = form_data.get('member5_roll', '').strip() or None
        
        member6_name = form_data.get('member6_name', '').strip() or None
        member6_email = form_data.get('member6_email', '').strip() or None
        member6_phone = form_data.get('member6_phone', '').strip() or None
        member6_roll = form_data.get('member6_roll', '').strip() or None
        
        leader_value = form_data.get('leader')
        
        # Validation
        if not team_name:
            errors.append('Team name is required.')
        if not college:
            errors.append('College is required.')
        if not branch:
            errors.append('Branch is required.')
        if not year_of_study:
            errors.append('Year of study is required.')
        if not idea_title:
            errors.append('Idea title is required.')
        if not idea_theme:
            errors.append('Idea theme is required.')
        if not ppt_upload_url:
            errors.append('PPT upload is required.')
        if not member1_name or not member1_email or not member1_phone or not member1_roll:
            errors.append('Member 1 details (including roll number) are required.')
        if not member2_name or not member2_email or not member2_phone or not member2_roll:
            errors.append('Member 2 details (including roll number) are required.')
        if not member3_name or not member3_email or not member3_phone or not member3_roll:
            errors.append('Member 3 details (including roll number) are required.')
        if not member4_name or not member4_email or not member4_phone or not member4_roll:
            errors.append('Member 4 details (including roll number) are required.')
        if not leader_value:
            errors.append('Please select exactly one team leader.')
        if leader_value in ['5', '6']:
            if leader_value == '5' and not member5_name:
                errors.append('Member 5 cannot be leader without name.')
            if leader_value == '6' and not member6_name:
                errors.append('Member 6 cannot be leader without name.')
        
        leader_index = None
        if leader_value:
            try:
                leader_index = int(leader_value)
            except ValueError:
                errors.append('Invalid leader selection.')
        
        is_leader1 = leader_index == 1
        is_leader2 = leader_index == 2
        is_leader3 = leader_index == 3
        is_leader4 = leader_index == 4
        is_leader5 = leader_index == 5
        is_leader6 = leader_index == 6
        
        leader_count = sum([
            int(is_leader1),
            int(is_leader2),
            int(is_leader3),
            int(is_leader4),
            int(is_leader5),
            int(is_leader6),
        ])
        
        if leader_count != 1:
            errors.append('Please select exactly one team leader.')
        
        if errors:
            return render(
                request,
                'website/register.html',
                {'errors': errors, 'form_data': form_data},
            )
        
        # Database insertion
        conn_str = os.environ.get('NEON_DATABASE_URL')
        if not conn_str:
            errors.append('Database configuration is missing. Please contact the organizer.')
            return render(
                request,
                'website/register.html',
                {'errors': errors, 'form_data': form_data},
            )
        
        try:
            conn = psycopg2.connect(conn_str)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO codestorm_registrations (
                    team_name,
                    college,
                    branch,
                    year_of_study,
                    idea_title,
                    idea_theme,
                    ppt_upload_url,
                    youtube_link,
                    member1_name,
                    member1_email,
                    member1_phone,
                    member1_roll,
                    is_leader1,
                    member2_name,
                    member2_email,
                    member2_phone,
                    member2_roll,
                    is_leader2,
                    member3_name,
                    member3_email,
                    member3_phone,
                    member3_roll,
                    is_leader3,
                    member4_name,
                    member4_email,
                    member4_phone,
                    member4_roll,
                    is_leader4,
                    member5_name,
                    member5_email,
                    member5_phone,
                    member5_roll,
                    is_leader5,
                    member6_name,
                    member6_email,
                    member6_phone,
                    member6_roll,
                    is_leader6
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                """,
                [
                    team_name,
                    college,
                    branch,
                    year_of_study,
                    idea_title,
                    idea_theme,
                    ppt_upload_url,
                    youtube_link,
                    member1_name,
                    member1_email,
                    member1_phone,
                    member1_roll,
                    is_leader1,
                    member2_name,
                    member2_email,
                    member2_phone,
                    member2_roll,
                    is_leader2,
                    member3_name,
                    member3_email,
                    member3_phone,
                    member3_roll,
                    is_leader3,
                    member4_name,
                    member4_email,
                    member4_phone,
                    member4_roll,
                    is_leader4,
                    member5_name,
                    member5_email,
                    member5_phone,
                    member5_roll,
                    is_leader5,
                    member6_name,
                    member6_email,
                    member6_phone,
                    member6_roll,
                    is_leader6,
                ],
            )
            conn.commit()
            cur.close()
            conn.close()
            
        except IntegrityError:
            errors.append('A team with this name has already registered.')
            return render(
                request,
                'website/register.html',
                {'errors': errors, 'form_data': form_data},
            )
        except Exception as e:
            errors.append(f'An unexpected error occurred while saving your registration: {str(e)}')
            return render(
                request,
                'website/register.html',
                {'errors': errors, 'form_data': form_data},
            )
        
        return render(
            request,
            'website/register.html',
            {'success': True},
        )
    
    return render(request, 'website/register.html')
