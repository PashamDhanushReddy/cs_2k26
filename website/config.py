import os
from pathlib import Path

# Supabase Configuration
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://your-project.supabase.co')
SUPABASE_ANON_KEY = os.environ.get('SUPABASE_ANON_KEY', 'your-anon-key')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', 'your-service-key')

# Storage Configuration
STORAGE_BUCKET_NAME = 'codestorm-ppt'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = [
    'application/vnd.ms-powerpoint',  # .ppt
    'application/vnd.openxmlformats-officedocument.presentationml.presentation'  # .pptx
]

# Registration Settings
MAX_TEAM_SIZE = 6
MIN_TEAM_SIZE = 4

# Validation Messages
VALIDATION_MESSAGES = {
    'REQUIRED_FIELD': 'This field is required',
    'INVALID_FILE_TYPE': 'Please upload a valid PPT file (.ppt or .pptx)',
    'FILE_TOO_LARGE': 'File size must be less than 10MB',
    'INVALID_EMAIL': 'Please enter a valid email address',
    'INVALID_PHONE': 'Please enter a valid phone number',
    'TEAM_LEADER_REQUIRED': 'Please select a team leader',
    'REGISTRATION_FAILED': 'Registration failed. Please try again.',
    'UPLOAD_FAILED': 'File upload failed. Please try again.'
}