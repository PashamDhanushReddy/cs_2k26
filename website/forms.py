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

class TeamRegistrationForm(forms.Form):
    # Team details
    team_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your team name'
        })
    )
    team_size = forms.ChoiceField(
        choices=[
            ('', 'Select Team Size'),
            ('4', '4 Members'),
            ('5', '5 Members'),
            ('6', '6 Members'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'id': 'team_size'
        })
    )
    # Idea details
    idea_title = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
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
            'class': 'form-control form-select'
        })
    )
    
    # File uploads
    ppt_file = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['ppt', 'pptx', 'pdf'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.ppt,.pptx,.pdf'
        })
    )
    youtube_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter YouTube link'
        })
    )
    
    # Member 1 (Required)
    member1_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    member1_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    member1_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
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
            'class': 'form-control',
            'placeholder': 'Roll Number'
        })
    )
    member1_gender = forms.ChoiceField(
        choices=[
            ('unspecified', 'Unspecified'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        initial='unspecified',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member1_college_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Name (if different from team college)'
        })
    )
    member1_course_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Course Name (e.g., B.Tech CSE)'
        })
    )
    member1_year = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member1_college_code = forms.CharField(
        max_length=50,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Code (e.g., ABC)'
        })
    )
    is_leader1 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(1)'
        })
    )
    
    # Member 2 (Required)
    member2_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    member2_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    member2_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
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
            'class': 'form-control',
            'placeholder': 'Roll Number'
        })
    )
    member2_gender = forms.ChoiceField(
        choices=[
            ('unspecified', 'Unspecified'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        initial='unspecified',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member2_college_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Name (if different from team college)'
        })
    )
    member2_course_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Course Name (e.g., B.Tech CSE)'
        })
    )
    member2_year = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member2_college_code = forms.CharField(
        max_length=50,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Code (e.g., ABC)'
        })
    )
    is_leader2 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(2)'
        })
    )
    
    # Member 3 (Required)
    member3_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    member3_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    member3_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
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
            'class': 'form-control',
            'placeholder': 'Roll Number'
        })
    )
    member3_gender = forms.ChoiceField(
        choices=[
            ('unspecified', 'Unspecified'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        initial='unspecified',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member3_college_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Name (if different from team college)'
        })
    )
    member3_course_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Course Name (e.g., B.Tech CSE)'
        })
    )
    member3_year = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member3_college_code = forms.CharField(
        max_length=50,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Code (e.g., ABC)'
        })
    )
    is_leader3 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(3)'
        })
    )
    
    # Member 4 (Required)
    member4_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    member4_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    member4_phone = forms.CharField(
        max_length=10,
        min_length=10,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
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
            'class': 'form-control',
            'placeholder': 'Roll Number'
        })
    )
    member4_gender = forms.ChoiceField(
        choices=[
            ('unspecified', 'Unspecified'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        initial='unspecified',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member4_college_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Name (if different from team college)'
        })
    )
    member4_course_name = forms.CharField(
        max_length=255,
        initial='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Course Name (e.g., B.Tech CSE)'
        })
    )
    member4_year = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        initial='',
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member4_college_code = forms.CharField(
        max_length=50,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Code (e.g., ABC)'
        })
    )
    is_leader4 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(4)'
        })
    )
    
    # Member 5
    member5_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Full Name'
        })
    )
    member5_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address (Optional)'
        })
    )
    member5_phone = forms.CharField(
        max_length=10,
        min_length=10,
        required=False,
        validators=[validate_indian_phone],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone Number (10 digits, start with 6-9) (Optional)',
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
            'class': 'form-control',
            'placeholder': 'Roll Number (Optional)'
        })
    )
    member5_gender = forms.ChoiceField(
        choices=[
            ('', 'Select Gender'),
            ('unspecified', 'Unspecified'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member5_college_name = forms.CharField(
        max_length=255,
        initial='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Name (if different from team college) (Optional)'
        })
    )
    member5_course_name = forms.CharField(
        max_length=255,
        initial='',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Course Name (e.g., B.Tech CSE) (Optional)'
        })
    )
    member5_year = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        initial='',
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-select'
        })
    )
    member5_college_code = forms.CharField(
        max_length=50,
        required=False,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College Code (e.g., ABC) (Optional)'
        })
    )
    is_leader5 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(5)'
        })
    )
    
    # Member 6
    member6_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Full Name'
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
    member6_gender = forms.ChoiceField(
        choices=[
            ('', 'Select Gender'),
            ('unspecified', 'Unspecified'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500'
        })
    )
    member6_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name (if different from team college)'
        })
    )
    member6_course_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name (e.g., B.Tech CSE)'
        })
    )
    member6_year = forms.ChoiceField(
        choices=[
            ('', 'Select Year'),
            ('1', '1st Year'),
            ('2', '2nd Year'),
            ('3', '3rd Year'),
            ('4', '4th Year'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500'
        })
    )
    member6_college_code = forms.CharField(
        max_length=50,
        required=False,
        validators=[validate_capital_letters],
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code (e.g., ABC)'
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
        
        team_size = cleaned_data.get('team_size')
        
        # Collect all validation errors
        errors = []
        
        # Validate required members based on team size
        if team_size:
            required_members = int(team_size)
            
            # Validate members 1-4 are always required (minimum team size is 4)
            required_fields_member1 = ['member1_name', 'member1_email', 'member1_phone', 'member1_roll', 'member1_gender', 'member1_college_name', 'member1_college_code', 'member1_course_name', 'member1_year']
            required_fields_member2 = ['member2_name', 'member2_email', 'member2_phone', 'member2_roll', 'member2_gender', 'member2_college_name', 'member2_college_code', 'member2_course_name', 'member2_year']
            required_fields_member3 = ['member3_name', 'member3_email', 'member3_phone', 'member3_roll', 'member3_gender', 'member3_college_name', 'member3_college_code', 'member3_course_name', 'member3_year']
            required_fields_member4 = ['member4_name', 'member4_email', 'member4_phone', 'member4_roll', 'member4_gender', 'member4_college_name', 'member4_college_code', 'member4_course_name', 'member4_year']
            
            # Check required members
            for i in range(1, min(required_members + 1, 5)):  # Members 1-4
                member_fields = locals()[f'required_fields_member{i}']
                for field in member_fields:
                    if not cleaned_data.get(field):
                        errors.append(f'Member {i} details are required for team size {team_size}.')
                        break  # Only show one error per member
            
            # Check member 5 if team size is 5 or 6
            if required_members >= 5:
                required_fields_member5 = ['member5_name', 'member5_email', 'member5_phone', 'member5_roll', 'member5_gender', 'member5_college_name', 'member5_college_code', 'member5_course_name', 'member5_year']
                for field in required_fields_member5:
                    if not cleaned_data.get(field):
                        errors.append(f'Member 5 details are required for team size {team_size}.')
                        break  # Only show one error per member
            
            # Check member 6 if team size is 6
            if required_members == 6:
                required_fields_member6 = ['member6_name', 'member6_email', 'member6_phone', 'member6_roll', 'member6_gender', 'member6_college_name', 'member6_college_code', 'member6_course_name', 'member6_year']
                for field in required_fields_member6:
                    if not cleaned_data.get(field):
                        errors.append(f'Member 6 details are required for team size {team_size}.')
                        break  # Only show one error per member
        
        # Validate that exactly one leader is selected
        leader_fields = ['is_leader1', 'is_leader2', 'is_leader3', 'is_leader4', 'is_leader5', 'is_leader6']
        leader_count = sum(1 for field in leader_fields if cleaned_data.get(field))
        
        if leader_count != 1:
            errors.append('Exactly one team member must be designated as the leader.')
        
        # Validate optional members cannot be leaders if not provided
        if cleaned_data.get('is_leader5') and not cleaned_data.get('member5_name'):
            errors.append('Member 5 cannot be leader if not provided.')
        
        if cleaned_data.get('is_leader6') and not cleaned_data.get('member6_name'):
            errors.append('Member 6 cannot be leader if not provided.')
        
        # Validate that at least one female team member is present
        has_female_member = False
        
        # Check all members that have names (indicating they are provided)
        for i in range(1, 7):
            member_name = cleaned_data.get(f'member{i}_name')
            member_gender = cleaned_data.get(f'member{i}_gender')
            
            # Only check gender if member name is provided (member exists)
            if member_name and member_gender == 'female':
                has_female_member = True
                break
        
        if not has_female_member:
            errors.append('At least one team member must be female.')
        
        # Raise all collected errors
        if errors:
            raise forms.ValidationError(errors)
        
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