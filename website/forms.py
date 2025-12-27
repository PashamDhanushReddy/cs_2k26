from django import forms
from django.core.validators import FileExtensionValidator, RegexValidator
from django.core.exceptions import ValidationError
import re

def validate_indian_phone(value):
    """Validate Indian phone number format"""
    if len(value) != 10:
        raise ValidationError('Phone number must be exactly 10 digits.')
    if not value.isdigit():
        raise ValidationError('Phone number must contain only digits.')
    if value[0] not in '6789':
        raise ValidationError('Phone number must start with 6, 7, 8, or 9.')
    return value

def validate_capital_letters(value):
    """Validate that the input contains only capital letters."""
    if not re.fullmatch(r'[A-Z]+', value):
        raise ValidationError('This field must contain only capital letters.')
    return value

def validate_google_drive_link(value):
    """Validate Google Drive link format"""
    if not value.startswith('https://'):
        raise ValidationError('Link must start with https://')
    if 'drive.google.com' not in value and 'docs.google.com' not in value:
        raise ValidationError('Please provide a valid Google Drive link.')
    return value

class TeamRegistrationForm(forms.Form):
    # Team details
    team_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter your team name'
        })
    )
    college = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter your college name'
        })
    )
    college_code = forms.CharField(
        max_length=50,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter College Code (e.g., ABC)'
        })
    )
    branch = forms.ChoiceField(
        choices=[
            ('', 'Select Branch'),
            ('CSE', 'CSE'),
            ('CSE-CS', 'CSE-CS'),
            ('CSE-AIML', 'CSE-AIML'),
            ('CSE-DS', 'CSE-DS'),
            ('IT', 'IT'),
            ('EEE', 'EEE'),
            ('ECE', 'ECE'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500'
        })
    )
    year_of_study = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500'
        })
    )
    
    # Idea details
    idea_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter your idea title'
        })
    )
    idea_theme = forms.ChoiceField(
        choices=[
            ('', 'Select Theme'),
            ('Generative Al & LLM Applications', 'Generative Al & LLM Applications'),
            ('Robotics, Drones & Autonomous Systems', 'Robotics, Drones & Autonomous Systems'),
            ('Cybersecurity & Threat Intelligence', 'Cybersecurity & Threat Intelligence'),
            ('HealthTech, MedAl & Diagnostics', 'HealthTech, MedAl & Diagnostics'),
            ('FinTech, Blockchain & Digital Trust', 'FinTech, Blockchain & Digital Trust'),
            ('Smart Cities, IoT & Edge Computing', 'Smart Cities, IoT & Edge Computing'),
            ('Green Tech & Energy Optimization', 'Green Tech & Energy Optimization'),
            ('Agritech & Rural Innovation', 'Agritech & Rural Innovation'),
            ('Transportation & Logistics (Al-Driven)', 'Transportation & Logistics (Al-Driven)'),
            ('Open Innovation Challenge (Wildcard Track)', 'Open Innovation Challenge (Wildcard Track)'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500'
        })
    )
    
    # PPT Google Drive Link - stores directly in ppt_file_path column
    ppt_file_path = forms.URLField(
        required=True,
        validators=[validate_google_drive_link],
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter Google Drive link for your PPT (make sure link is publicly accessible)'
        })
    )
    youtube_link = forms.URLField(
        required=True,
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter YouTube link'
        })
    )
    
    # Member 1 (Required)
    member1_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name'
        })
    )
    member1_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Email Address'
        })
    )
    member1_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (10 digits, start with 6-9)',
            'type': 'tel',
            'pattern': '[6-9][0-9]{9}',
            'maxlength': '10',
            'minlength': '10',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, \'\').slice(0, 10)'
        })
    )
    member1_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    is_leader1 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-amber-600 bg-gray-800 border-gray-600 rounded focus:ring-amber-500',
            'onchange': 'updateLeaderCheckbox(1)'
        })
    )
    
    # Member 2 (Required)
    member2_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name'
        })
    )
    member2_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Email Address'
        })
    )
    member2_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (10 digits, start with 6-9)',
            'type': 'tel',
            'pattern': '[6-9][0-9]{9}',
            'maxlength': '10',
            'minlength': '10',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, \'\').slice(0, 10)'
        })
    )
    member2_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    is_leader2 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-amber-600 bg-gray-800 border-gray-600 rounded focus:ring-amber-500',
            'onchange': 'updateLeaderCheckbox(2)'
        })
    )
    
    # Member 3 (Required)
    member3_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name'
        })
    )
    member3_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Email Address'
        })
    )
    member3_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (10 digits, start with 6-9)',
            'type': 'tel',
            'pattern': '[6-9][0-9]{9}',
            'maxlength': '10',
            'minlength': '10',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, \'\').slice(0, 10)'
        })
    )
    member3_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    is_leader3 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-amber-600 bg-gray-800 border-gray-600 rounded focus:ring-amber-500',
            'onchange': 'updateLeaderCheckbox(3)'
        })
    )
    
    # Member 4 (Required)
    member4_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name'
        })
    )
    member4_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Email Address'
        })
    )
    member4_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (10 digits, start with 6-9)',
            'type': 'tel',
            'pattern': '[6-9][0-9]{9}',
            'maxlength': '10',
            'minlength': '10',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, \'\').slice(0, 10)'
        })
    )
    member4_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    is_leader4 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-amber-600 bg-gray-800 border-gray-600 rounded focus:ring-amber-500',
            'onchange': 'updateLeaderCheckbox(4)'
        })
    )
    
    # Member 5 (Optional)
    member5_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name (Optional)'
        })
    )
    member5_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Email Address (Optional)'
        })
    )
    member5_phone = forms.CharField(
        max_length=10,
        min_length=10,
        required=False,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (10 digits, start with 6-9)',
            'type': 'tel',
            'pattern': '[6-9][0-9]{9}',
            'maxlength': '10',
            'minlength': '10',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, \'\').slice(0, 10)'
        })
    )
    member5_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number (Optional)'
        })
    )
    is_leader5 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-amber-600 bg-gray-800 border-gray-600 rounded focus:ring-amber-500',
            'onchange': 'updateLeaderCheckbox(5)'
        })
    )
    
    # Member 6 (Optional)
    member6_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name (Optional)'
        })
    )
    member6_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Email Address (Optional)'
        })
    )
    member6_phone = forms.CharField(
        max_length=10,
        min_length=10,
        required=False,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (10 digits, start with 6-9)',
            'type': 'tel',
            'pattern': '[6-9][0-9]{9}',
            'maxlength': '10',
            'minlength': '10',
            'inputmode': 'numeric',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, \'\').slice(0, 10)'
        })
    )
    member6_roll = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number (Optional)'
        })
    )
    is_leader6 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-amber-600 bg-gray-800 border-gray-600 rounded focus:ring-amber-500',
            'onchange': 'updateLeaderCheckbox(6)'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        
        # Validate that exactly one leader is selected
        leader_fields = ['is_leader1', 'is_leader2', 'is_leader3', 'is_leader4', 'is_leader5', 'is_leader6']
        leader_count = sum(1 for field in leader_fields if cleaned_data.get(field))
        
        if leader_count != 1:
            raise forms.ValidationError('Exactly one team member must be designated as the leader.')
        
        # Validate optional members
        if cleaned_data.get('is_leader5') and not cleaned_data.get('member5_name'):
            raise forms.ValidationError('Member 5 cannot be leader if not provided.')
        
        if cleaned_data.get('is_leader6') and not cleaned_data.get('member6_name'):
            raise forms.ValidationError('Member 6 cannot be leader if not provided.')
        
        return cleaned_data

    def validate_phone_number(self, phone):
        """Validate Indian phone number format"""
        if not phone:
            return phone
        
        # Remove any spaces or special characters
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        # Check if it's a valid 10-digit Indian number
        if len(phone) != 10:
            raise forms.ValidationError('Phone number must be 10 digits.')
        
        # Check if it starts with valid digits (6-9 for Indian mobile numbers)
        if not phone[0] in '6789':
            raise forms.ValidationError('Phone number must start with 6, 7, 8, or 9.')
        
        # Check if all characters are digits
        if not phone.isdigit():
            raise forms.ValidationError('Phone number must contain only digits.')
        
        return phone

    def clean_member1_phone(self):
        return self.validate_phone_number(self.cleaned_data.get('member1_phone'))
    
    def clean_member2_phone(self):
        return self.validate_phone_number(self.cleaned_data.get('member2_phone'))
    
    def clean_member3_phone(self):
        return self.validate_phone_number(self.cleaned_data.get('member3_phone'))
    
    def clean_member4_phone(self):
        return self.validate_phone_number(self.cleaned_data.get('member4_phone'))
    
    def clean_member5_phone(self):
        return self.validate_phone_number(self.cleaned_data.get('member5_phone'))
    
    def clean_member6_phone(self):
        return self.validate_phone_number(self.cleaned_data.get('member6_phone'))