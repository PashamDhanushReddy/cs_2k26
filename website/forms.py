from django import forms
from django.core.validators import FileExtensionValidator

class TeamRegistrationForm(forms.Form):
    # Team details
    team_size = forms.ChoiceField(
        choices=[
            ('4', '4 Members'),
            ('5', '5 Members'),
            ('6', '6 Members')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    
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
    branch = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter your branch'
        })
    )
    year_of_study = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter year of study'
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
            ('Generative AI & LLM Applications', 'Generative AI & LLM Applications'),
            ('Robotics, Drones & Autonomous Systems', 'Robotics, Drones & Autonomous Systems'),
            ('Cybersecurity & Threat Intelligence', 'Cybersecurity & Threat Intelligence'),
            ('HealthTech, MedAI & Diagnostics', 'HealthTech, MedAI & Diagnostics'),
            ('FinTech, Blockchain & Digital Trust', 'FinTech, Blockchain & Digital Trust'),
            ('Smart Cities, IoT & Edge Computing', 'Smart Cities, IoT & Edge Computing'),
            ('Green Tech & Energy Optimization', 'Green Tech & Energy Optimization'),
            ('Agritech & Rural Innovation', 'Agritech & Rural Innovation'),
            ('Transportation & Logistics (AI-Driven)', 'Transportation & Logistics (AI-Driven)'),
            ('Open Innovation Challenge (Wildcard Track)', 'Open Innovation Challenge (Wildcard Track)')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500'
        })
    )
    
    # File uploads
    ppt_file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['ppt', 'pptx', 'pdf'])],
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'accept': '.ppt,.pptx,.pdf'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member1_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    member1_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member1_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code'
        })
    )
    member1_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name'
        })
    )
    member1_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member1_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member2_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    member2_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member2_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code'
        })
    )
    member2_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name'
        })
    )
    member2_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member2_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member3_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    member3_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member3_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code'
        })
    )
    member3_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name'
        })
    )
    member3_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member3_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
        })
    )
    member4_roll = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Roll Number'
        })
    )
    member4_gender = forms.ChoiceField(
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member4_college_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code'
        })
    )
    member4_course_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name'
        })
    )
    member4_year = forms.ChoiceField(
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member4_college_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name'
        })
    )
    is_leader4 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
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
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (Optional)',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
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
    member5_gender = forms.ChoiceField(
        required=False,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member5_college_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code (Optional)'
        })
    )
    member5_course_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name (Optional)'
        })
    )
    member5_year = forms.ChoiceField(
        required=False,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member5_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name (Optional)'
        })
    )
    is_leader5 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
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
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (Optional)',
            'type': 'tel',
            'maxlength': '10',
            'pattern': '[6-9][0-9]{9}'
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
        required=False,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member6_college_code = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Code (Optional)'
        })
    )
    member6_course_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Course Name (Optional)'
        })
    )
    member6_year = forms.ChoiceField(
        required=False,
        choices=[
            ('1st Year', '1st Year'),
            ('2nd Year', '2nd Year'),
            ('3rd Year', '3rd Year'),
            ('4th Year', '4th Year'),
            ('5th Year', '5th Year')
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
        })
    )
    member6_college_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'College Name (Optional)'
        })
    )
    is_leader6 = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'onchange': 'updateLeaderCheckbox(6)'
        })
    )

    def clean_member1_email(self):
        email = self.cleaned_data.get('member1_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member2_email(self):
        email = self.cleaned_data.get('member2_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member3_email(self):
        email = self.cleaned_data.get('member3_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member4_email(self):
        email = self.cleaned_data.get('member4_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member5_email(self):
        email = self.cleaned_data.get('member5_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email
    
    def clean_member6_email(self):
        email = self.cleaned_data.get('member6_email')
        if email:
            if not email.endswith('@') and '.' not in email.split('@')[-1]:
                raise forms.ValidationError('Please enter a valid email address.')
        return email

    def clean_member1_phone(self):
        phone = self.cleaned_data.get('member1_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member2_phone(self):
        phone = self.cleaned_data.get('member2_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member3_phone(self):
        phone = self.cleaned_data.get('member3_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member4_phone(self):
        phone = self.cleaned_data.get('member4_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member5_phone(self):
        phone = self.cleaned_data.get('member5_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone
    
    def clean_member6_phone(self):
        phone = self.cleaned_data.get('member6_phone')
        if phone:
            import re
            if not re.match(r'^[6-9]\d{9}$', phone):
                raise forms.ValidationError('Phone number must be 10 digits starting with 6, 7, 8, or 9.')
        return phone

    def clean_member1_college_code(self):
        college_code = self.cleaned_data.get('member1_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member1_college_name(self):
        college_name = self.cleaned_data.get('member1_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member1_course_name(self):
        course_name = self.cleaned_data.get('member1_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member2_college_code(self):
        college_code = self.cleaned_data.get('member2_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member2_college_name(self):
        college_name = self.cleaned_data.get('member2_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member2_course_name(self):
        course_name = self.cleaned_data.get('member2_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member3_college_code(self):
        college_code = self.cleaned_data.get('member3_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member3_college_name(self):
        college_name = self.cleaned_data.get('member3_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member3_course_name(self):
        course_name = self.cleaned_data.get('member3_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member4_college_code(self):
        college_code = self.cleaned_data.get('member4_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member4_college_name(self):
        college_name = self.cleaned_data.get('member4_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member4_course_name(self):
        course_name = self.cleaned_data.get('member4_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member5_college_code(self):
        college_code = self.cleaned_data.get('member5_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member5_college_name(self):
        college_name = self.cleaned_data.get('member5_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member5_course_name(self):
        course_name = self.cleaned_data.get('member5_course_name')
        if course_name:
            return course_name.upper()
        return course_name

    def clean_member6_college_code(self):
        college_code = self.cleaned_data.get('member6_college_code')
        if college_code:
            return college_code.upper()
        return college_code
    
    def clean_member6_college_name(self):
        college_name = self.cleaned_data.get('member6_college_name')
        if college_name:
            return college_name.upper()
        return college_name
    
    def clean_member6_course_name(self):
        course_name = self.cleaned_data.get('member6_course_name')
        if course_name:
            return course_name.upper()
        return course_name

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