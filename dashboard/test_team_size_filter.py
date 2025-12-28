from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from dashboard.views import dashboard_view

class TeamSizeFilterTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @patch('dashboard.views.get_supabase_client')
    def test_team_size_filter_4_members(self, mock_get_supabase):
        """Test filtering by team size 4"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data with different team sizes
        mock_data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'idea_theme': 'Theme1', 'ppt_file_path': None},
            {'id': 2, 'college_code': 'CC2', 'member1_name': 'Team2', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'member5_name': 'Member5', 
             'idea_theme': 'Theme2', 'ppt_file_path': None},
            {'id': 3, 'college_code': 'CC3', 'member1_name': 'Team3', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'member5_name': 'Member5', 
             'member6_name': 'Member6', 'idea_theme': 'Theme3', 'ppt_file_path': None},
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
        
        # Create request with team size filter
        request = self.factory.get('/dashboard/?team_size=4')
        request.user = self.user
        
        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Should only show teams with 4 members
            self.assertEqual(len(context['registrations']), 1)
            self.assertEqual(context['registrations'][0]['team_size'], 4)
            
            print(f"Teams with 4 members: {len(context['registrations'])}")
            print(f"Team sizes in result: {[reg['team_size'] for reg in context['registrations']]}")

    @patch('dashboard.views.get_supabase_client')
    def test_team_size_filter_5_members(self, mock_get_supabase):
        """Test filtering by team size 5"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data with different team sizes
        mock_data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'idea_theme': 'Theme1', 'ppt_file_path': None},
            {'id': 2, 'college_code': 'CC2', 'member1_name': 'Team2', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'member5_name': 'Member5', 
             'idea_theme': 'Theme2', 'ppt_file_path': None},
            {'id': 3, 'college_code': 'CC3', 'member1_name': 'Team3', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'member5_name': 'Member5', 
             'member6_name': 'Member6', 'idea_theme': 'Theme3', 'ppt_file_path': None},
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
        
        # Create request with team size filter
        request = self.factory.get('/dashboard/?team_size=5')
        request.user = self.user
        
        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Should only show teams with 5 members
            self.assertEqual(len(context['registrations']), 1)
            self.assertEqual(context['registrations'][0]['team_size'], 5)
            
            print(f"Teams with 5 members: {len(context['registrations'])}")
            print(f"Team sizes in result: {[reg['team_size'] for reg in context['registrations']]}")

    @patch('dashboard.views.get_supabase_client')
    def test_team_size_filter_no_filter(self, mock_get_supabase):
        """Test with no team size filter - should show all teams"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data with different team sizes
        mock_data = [
            {'id': 1, 'college_code': 'CC1', 'member1_name': 'Team1', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'idea_theme': 'Theme1', 'ppt_file_path': None},
            {'id': 2, 'college_code': 'CC2', 'member1_name': 'Team2', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'member5_name': 'Member5', 
             'idea_theme': 'Theme2', 'ppt_file_path': None},
            {'id': 3, 'college_code': 'CC3', 'member1_name': 'Team3', 'member2_name': 'Member2', 
             'member3_name': 'Member3', 'member4_name': 'Member4', 'member5_name': 'Member5', 
             'member6_name': 'Member6', 'idea_theme': 'Theme3', 'ppt_file_path': None},
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
        
        # Create request with no team size filter
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Should show all teams
            self.assertEqual(len(context['registrations']), 3)
            team_sizes = [reg['team_size'] for reg in context['registrations']]
            self.assertIn(4, team_sizes)
            self.assertIn(5, team_sizes)
            self.assertIn(6, team_sizes)
            
            print(f"All teams (no filter): {len(context['registrations'])}")
            print(f"Team sizes in result: {team_sizes}")