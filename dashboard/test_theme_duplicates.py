from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from dashboard.views import dashboard_view

class TestThemeDuplicates(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    @patch('dashboard.views.get_supabase_client')
    def test_theme_duplicates_issue(self, mock_get_supabase):
        """Test to identify and fix theme duplication issues"""
        # Mock Supabase response with duplicate themes (including whitespace/case variations)
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data with potential duplicate themes
        mock_data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'idea_theme': 'Generative AI & LLM Applications', 'ppt_file_path': None},
            {'id': 2, 'college_code': 'CC2', 'member1_name': 'Team2', 'idea_theme': 'Cybersecurity & Threat Intelligence', 'ppt_file_path': None}, 
            {'id': 3, 'college_code': 'CC1', 'member1_name': 'Team3', 'idea_theme': 'Generative AI & LLM Applications ', 'ppt_file_path': None},  # Note the trailing space
            {'id': 4, 'college_code': 'CC3', 'member1_name': 'Team4', 'idea_theme': 'Cybersecurity & Threat Intelligence', 'ppt_file_path': None},
            {'id': 5, 'college_code': 'CC1', 'member1_name': 'Team5', 'idea_theme': 'Generative AI & LLM Applications', 'ppt_file_path': None},
        ]
        
        mock_response = MagicMock()
        mock_response.data = mock_data
        mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response
        
        # Create request
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        # Mock render to capture context
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Check idea themes
            idea_themes = context['idea_themes']
            print(f"All idea themes: {idea_themes}")
            print(f"Number of themes: {len(idea_themes)}")
            
            # Check for duplicates
            seen = set()
            duplicates = []
            for theme in idea_themes:
                if theme in seen:
                    duplicates.append(theme)
                else:
                    seen.add(theme)
            
            if duplicates:
                print(f"Duplicate themes found: {duplicates}")
            else:
                print("No duplicates found")
                
            # Verify the expected themes are present
            expected_themes = [
                'Generative AI & LLM Applications',
                'Cybersecurity & Threat Intelligence'
            ]
            
            for expected_theme in expected_themes:
                count = sum(1 for theme in idea_themes if theme.strip() == expected_theme)
                print(f"'{expected_theme}' appears {count} times")
                
            # Assert no duplicates (after stripping whitespace)
            stripped_themes = [theme.strip() for theme in idea_themes]
            unique_themes = set(stripped_themes)
            print(f"Unique themes count: {len(unique_themes)}")
            print(f"Total themes count: {len(stripped_themes)}")
            
            self.assertEqual(len(stripped_themes), len(unique_themes), 
                           f"Found duplicate themes: {stripped_themes}")
            
            # Verify that 'Generative AI & LLM Applications' appears only once after stripping
            generative_ai_count = sum(1 for theme in stripped_themes if theme == 'Generative AI & LLM Applications')
            self.assertEqual(generative_ai_count, 1, 
                           f"'Generative AI & LLM Applications' should appear exactly once, but found {generative_ai_count} times")