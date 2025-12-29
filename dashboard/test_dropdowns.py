from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from dashboard.views import dashboard_view

class DashboardDropdownTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @patch('dashboard.views.get_supabase_client')
    def test_dropdowns_show_all_options(self, mock_get_supabase):
        """Test that dropdowns show all available options regardless of database content"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock empty database response (no registrations)
        mock_query = MagicMock()
        mock_response = MagicMock()
        mock_response.data = []  # Empty database
        mock_query.execute.return_value = mock_response
        mock_supabase.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.ilike.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.gte.return_value = mock_query
        mock_query.lte.return_value = mock_query
        
        # Create request
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Check team sizes show all options (4, 5, 6)
            self.assertEqual(context['team_sizes'], ['4', '5', '6'])
            
            # Check that idea themes include standard themes
            idea_themes = context['idea_themes']
            self.assertIn('Generative AI & LLM Applications', idea_themes)
            self.assertIn('Smart Cities, IoT & Edge Computing', idea_themes)
            self.assertIn('Cybersecurity & Threat Intelligence', idea_themes)
            
            print(f"Available team sizes: {context['team_sizes']}")
            print(f"Number of idea themes: {len(idea_themes)}")
            print(f"Sample themes: {idea_themes[:5]}")

    @patch('dashboard.views.get_supabase_client')
    def test_dropdowns_with_database_themes(self, mock_get_supabase):
        """Test that dropdowns show only standard themes, ignoring database themes"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock database with some themes
        mock_query = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'idea_theme': 'Custom Theme 1', 'ppt_file_path': None},
            {'id': 2, 'college_code': 'CC2', 'member1_name': 'Team2', 'idea_theme': 'Custom Theme 2', 'ppt_file_path': None},
        ]
        mock_query.execute.return_value = mock_response
        mock_supabase.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.ilike.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.gte.return_value = mock_query
        mock_query.lte.return_value = mock_query
        
        # Create request
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Check team sizes show all options
            self.assertEqual(context['team_sizes'], ['4', '5', '6'])
            
            # Check that only standard themes are included (database themes ignored)
            idea_themes = context['idea_themes']
            self.assertNotIn('Custom Theme 1', idea_themes)
            self.assertNotIn('Custom Theme 2', idea_themes)
            self.assertIn('Generative AI & LLM Applications', idea_themes)
            self.assertIn('Cybersecurity & Threat Intelligence', idea_themes)
