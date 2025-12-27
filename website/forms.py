from django import forms
from django.core.validators import FileExtensionValidator

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
    idea_theme = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter your idea theme/track'
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
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Enter YouTube link (optional)'
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
            'placeholder': 'Phone Number'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number'
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
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number'
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
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (Optional)'
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
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-amber-500 focus:ring-1 focus:ring-amber-500',
            'placeholder': 'Phone Number (Optional)'
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