from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from dashboard.views import dashboard_view
import json

class DashboardViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='password')

    @patch('dashboard.views.get_supabase_client')
    def test_total_registrations_shows_database_total(self, mock_get_supabase):
        # Mock Supabase response
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data - simulate 5 total registrations in database
        # but only 2 match the current filters
        mock_all_data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'idea_theme': 'Theme1', 'ppt_file_path': None},
            {'id': 2, 'college_code': 'CC2', 'member1_name': 'Team2', 'idea_theme': 'Theme2', 'ppt_file_path': None}, 
            {'id': 3, 'college_code': 'CC1', 'member1_name': 'Team3', 'idea_theme': 'Theme1', 'ppt_file_path': None},
            {'id': 4, 'college_code': 'CC3', 'member1_name': 'Team4', 'idea_theme': 'Theme3', 'ppt_file_path': None},
            {'id': 5, 'college_code': 'CC1', 'member1_name': 'Team5', 'idea_theme': 'Theme1', 'ppt_file_path': None},
        ]
        
        mock_filtered_data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'idea_theme': 'Theme1', 'ppt_file_path': None},
            {'id': 3, 'college_code': 'CC1', 'member1_name': 'Team3', 'idea_theme': 'Theme1', 'ppt_file_path': None},
        ]
        
        # Setup mocks for filtered query
        mock_filtered_query = MagicMock()
        mock_filtered_response = MagicMock()
        mock_filtered_response.data = mock_filtered_data
        mock_filtered_query.execute.return_value = mock_filtered_response
        
        # Setup mocks for all registrations query (unfiltered)
        mock_all_query = MagicMock()
        mock_all_response = MagicMock()
        mock_all_response.data = mock_all_data
        mock_all_query.execute.return_value = mock_all_response
        
        # Configure supabase mock
        mock_supabase.table.side_effect = [mock_filtered_query, mock_all_query]
        mock_filtered_query.select.return_value = mock_filtered_query
        mock_filtered_query.ilike.return_value = mock_filtered_query
        mock_filtered_query.eq.return_value = mock_filtered_query
        mock_filtered_query.gte.return_value = mock_filtered_query
        mock_filtered_query.lte.return_value = mock_filtered_query
        
        mock_all_query.select.return_value = mock_all_query
        
        # Create request with filters
        request = self.factory.get('/dashboard/?college_code=CC1')
        request.user = self.user

        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Check total_registrations shows database total (5), not filtered count (2)
            self.assertEqual(context['total_registrations'], 5)
            
            # Check filtered registrations count
            self.assertEqual(len(context['registrations']), 2)