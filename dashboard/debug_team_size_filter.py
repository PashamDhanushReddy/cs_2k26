from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from dashboard.views import dashboard_view

class DebugTeamSizeFilterTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @patch('dashboard.views.get_supabase_client')
    def test_debug_team_size_filter(self, mock_get_supabase):
        """Debug test to see what's happening with team size filter"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data with exactly 4 members
        mock_data = [
            {
                'id': 1, 
                'college_code': 'CC1', 
                'member1_name': 'Team1 Leader',
                'member2_name': 'Member2',
                'member3_name': 'Member3', 
                'member4_name': 'Member4',
                'member5_name': '',  # Empty
                'member6_name': '',  # Empty
                'idea_theme': 'Theme1', 
                'ppt_file_path': None
            },
        ]
        
        # Setup mocks
        mock_query = MagicMock()
        mock_response = MagicMock()
        mock_response.data = mock_data
        mock_query.execute.return_value = mock_response
        mock_supabase.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.ilike.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.gte.return_value = mock_query
        mock_query.lte.return_value = mock_query
        
        # Test with team_size=4 filter
        print("=== Testing with team_size=4 filter ===")
        request = self.factory.get('/dashboard/?team_size=4')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Filter value: '{request.GET.get('team_size')}'")
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                print(f"First result team size: {context['registrations'][0]['team_size']}")
            print(f"Context filters: {context['filters']}")
            
            # Should show 1 result
            self.assertEqual(len(context['registrations']), 1)
            
        # Test with team_size=5 filter (should show 0 results)
        print("\n=== Testing with team_size=5 filter ===")
        request = self.factory.get('/dashboard/?team_size=5')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Filter value: '{request.GET.get('team_size')}'")
            print(f"Number of results: {len(context['registrations'])}")
            print(f"Context filters: {context['filters']}")
            
            # Should show 0 results
            self.assertEqual(len(context['registrations']), 0)
            
        # Test with no filter (should show 1 result)
        print("\n=== Testing with no team size filter ===")
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Filter value: '{request.GET.get('team_size')}'")
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                print(f"First result team size: {context['registrations'][0]['team_size']}")
            print(f"Context filters: {context['filters']}")
            
            # Should show 1 result
            self.assertEqual(len(context['registrations']), 1)