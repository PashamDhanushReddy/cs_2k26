# CodeStorm 2026 - Registration System

A Django-based registration system for CodeStorm 2026 hackathon with Supabase integration for data storage and file uploads.

## Features

- **Multi-step Registration Form**: User-friendly 3-step registration process
- **PPT File Upload**: Direct upload to Supabase Storage bucket
- **Team Management**: Support for 4-6 team members with team leader selection
- **Form Validation**: Comprehensive client and server-side validation
- **Responsive Design**: Mobile-friendly interface with modern UI
- **Supabase Integration**: Secure data storage and file management

## Setup Instructions

### 1. Environment Variables

Copy the example environment file and update with your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env` with your Supabase project details:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here
SECRET_KEY=your-django-secret-key
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Run migrations:

```bash
python manage.py migrate
```

### 4. Supabase Configuration

#### Create Storage Bucket
1. Go to Supabase Dashboard → Storage
2. Create a new bucket named `codestorm-ppt`
3. Keep it private (not public)

#### Create Storage Policies

Create these policies in Supabase SQL Editor:

```sql
-- Allow uploads for authenticated users
create policy "Allow uploads" 
on storage.objects for insert 
to authenticated 
with check (bucket_id = 'codestorm-ppt');

-- Allow read access for authenticated users
create policy "Allow read access" 
on storage.objects for select 
to authenticated 
using (bucket_id = 'codestorm-ppt');
```

#### Create Registration Table

Run this SQL in Supabase SQL Editor:

```sql
CREATE TABLE codestorm_registrations (
    id BIGSERIAL PRIMARY KEY,
    
    -- Team details
    team_name VARCHAR(255) NOT NULL UNIQUE,
    college VARCHAR(255) NOT NULL,
    branch VARCHAR(255),
    year_of_study VARCHAR(50),
    
    -- Idea details
    idea_title VARCHAR(255) NOT NULL,
    idea_theme VARCHAR(255) NOT NULL,
    
    -- PPT stored in Supabase bucket (store file path, not URL)
    ppt_file_path TEXT NOT NULL,
    youtube_link VARCHAR(500),
    
    -- Member 1 (Required)
    member1_name VARCHAR(255) NOT NULL,
    member1_email VARCHAR(255) NOT NULL,
    member1_phone VARCHAR(20) NOT NULL,
    member1_roll VARCHAR(50) NOT NULL,
    is_leader1 BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Member 2 (Required)
    member2_name VARCHAR(255) NOT NULL,
    member2_email VARCHAR(255) NOT NULL,
    member2_phone VARCHAR(20) NOT NULL,
    member2_roll VARCHAR(50) NOT NULL,
    is_leader2 BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Member 3 (Required)
    member3_name VARCHAR(255) NOT NULL,
    member3_email VARCHAR(255) NOT NULL,
    member3_phone VARCHAR(20) NOT NULL,
    member3_roll VARCHAR(50) NOT NULL,
    is_leader3 BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Member 4 (Required)
    member4_name VARCHAR(255) NOT NULL,
    member4_email VARCHAR(255) NOT NULL,
    member4_phone VARCHAR(20) NOT NULL,
    member4_roll VARCHAR(50) NOT NULL,
    is_leader4 BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Member 5 (Optional)
    member5_name VARCHAR(255),
    member5_email VARCHAR(255),
    member5_phone VARCHAR(20),
    member5_roll VARCHAR(50),
    is_leader5 BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Member 6 (Optional)
    member6_name VARCHAR(255),
    member6_email VARCHAR(255),
    member6_phone VARCHAR(20),
    member6_roll VARCHAR(50),
    is_leader6 BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Constraints
    -- exactly ONE leader across all members
    CHECK (
        (CASE WHEN is_leader1 THEN 1 ELSE 0 END) +
        (CASE WHEN is_leader2 THEN 1 ELSE 0 END) +
        (CASE WHEN is_leader3 THEN 1 ELSE 0 END) +
        (CASE WHEN is_leader4 THEN 1 ELSE 0 END) +
        (CASE WHEN is_leader5 THEN 1 ELSE 0 END) +
        (CASE WHEN is_leader6 THEN 1 ELSE 0 END)
        = 1
    ),
    
    -- optional members cannot be leader if not filled
    CHECK (NOT is_leader5 OR member5_name IS NOT NULL),
    CHECK (NOT is_leader6 OR member6_name IS NOT NULL)
);
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/register` to access the registration form.

## API Endpoints

- `GET /register/` - Registration form page
- `POST /api/upload-ppt/` - Get signed URL for PPT upload
- `POST /api/submit-registration/` - Submit registration data

## File Structure

```
website/
├── templates/
│   └── website/
│       ├── home.html          # Homepage
│       └── register.html      # Registration form
├── config.py                  # Configuration settings
├── views.py                   # View functions and API endpoints
└── urls.py                    # URL routing
```

## Security Features

- CSRF protection on all forms
- Server-side validation
- File type and size validation
- Unique file naming to prevent conflicts
- Environment variable protection for sensitive data

## Troubleshooting

### Common Issues

1. **Supabase Connection Error**
   - Verify your SUPABASE_URL and keys are correct
   - Check network connectivity
   - Ensure RLS policies are properly configured

2. **File Upload Fails**
   - Check file size (max 10MB)
   - Verify file type (.ppt or .pptx)
   - Ensure storage bucket exists and policies are set

3. **Registration Validation Error**
   - All required fields must be filled
   - Exactly one team leader must be selected
   - Email addresses must be valid
   - Phone numbers must be at least 10 digits

### Environment Variables

Make sure these are set in your environment:

- `SUPABASE_URL`: Your Supabase project URL
- `SUPABASE_ANON_KEY`: Your Supabase anon key
- `SUPABASE_SERVICE_KEY`: Your Supabase service role key
- `SECRET_KEY`: Django secret key

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your Supabase configuration
3. Check browser console for JavaScript errors
4. Review Django logs for server-side issues