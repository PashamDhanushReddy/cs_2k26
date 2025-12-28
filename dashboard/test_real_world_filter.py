from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from unittest.mock import patch, MagicMock
from dashboard.views import dashboard_view

class RealWorldTeamSizeFilterTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    @patch('dashboard.views.get_supabase_client')
    def test_team_size_filter_with_ppt_data(self, mock_get_supabase):
        """Test team size filter with realistic data including PPT paths"""
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data with different team sizes and PPT files
        mock_data = [
            {
                'id': 1, 
                'college_code': 'CC1', 
                'team_name': 'Team Alpha',
                'member1_name': 'Leader1',
                'member2_name': 'Member2',
                'member3_name': 'Member3', 
                'member4_name': 'Member4',
                'member5_name': '',  # Empty - team size 4
                'member6_name': '',  # Empty
                'is_leader1': True,
                'idea_theme': 'AI/ML', 
                'ppt_file_path': 'presentations/team1.pptx',
                'selection_status': 'pending',
                'registration_date': '2023-01-01T12:00:00'
            },
            {
                'id': 2, 
                'college_code': 'CC2', 
                'team_name': 'Team Beta',
                'member1_name': 'Leader2',
                'member2_name': 'Member2',
                'member3_name': 'Member3', 
                'member4_name': 'Member4',
                'member5_name': 'Member5',  # 5 members
                'member6_name': '',  # Empty - team size 5
                'is_leader1': True,
                'idea_theme': 'Web Dev', 
                'ppt_file_path': None,  # No PPT
                'selection_status': 'selected',
                'registration_date': '2023-01-02T12:00:00'
            },
            {
                'id': 3, 
                'college_code': 'CC3', 
                'team_name': 'Team Gamma',
                'member1_name': 'Leader3',
                'member2_name': 'Member2',
                'member3_name': 'Member3', 
                'member4_name': 'Member4',
                'member5_name': 'Member5',  # 6 members
                'member6_name': 'Member6',  # team size 6
                'is_leader1': True,
                'idea_theme': 'Blockchain', 
                'ppt_file_path': 'presentations/team3.pptx',
                'selection_status': 'rejected',
                'registration_date': '2023-01-03T12:00:00'
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
        
        # Mock storage for PPT URLs
        mock_storage = MagicMock()
        mock_supabase.storage.from_.return_value = mock_storage
        mock_storage.create_signed_url.return_value = {'signedURL': 'http://example.com/signed-url'}
        
        print("=== Test 1: Filter by team size 4 (should show 1 result) ===")
        request = self.factory.get('/dashboard/?team_size=4')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                for i, reg in enumerate(context['registrations']):
                    print(f"Result {i+1}: {reg['team_name']} - Team size: {reg['team_size']}")
            print(f"Context filters: {context['filters']}")
            
            self.assertEqual(len(context['registrations']), 1)
            self.assertEqual(context['registrations'][0]['team_size'], 4)
            
        print("\n=== Test 2: Filter by team size 5 (should show 1 result) ===")
        request = self.factory.get('/dashboard/?team_size=5')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                for i, reg in enumerate(context['registrations']):
                    print(f"Result {i+1}: {reg['team_name']} - Team size: {reg['team_size']}")
            print(f"Context filters: {context['filters']}")
            
            self.assertEqual(len(context['registrations']), 1)
            self.assertEqual(context['registrations'][0]['team_size'], 5)
            
        print("\n=== Test 3: Filter by team size 6 (should show 1 result) ===")
        request = self.factory.get('/dashboard/?team_size=6')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                for i, reg in enumerate(context['registrations']):
                    print(f"Result {i+1}: {reg['team_name']} - Team size: {reg['team_size']}")
            print(f"Context filters: {context['filters']}")
            
            self.assertEqual(len(context['registrations']), 1)
            self.assertEqual(context['registrations'][0]['team_size'], 6)
            
        print("\n=== Test 4: No filter (should show all 3 results) ===")
        request = self.factory.get('/dashboard/')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                for i, reg in enumerate(context['registrations']):
                    print(f"Result {i+1}: {reg['team_name']} - Team size: {reg['team_size']}")
            print(f"Context filters: {context['filters']}")
            
            self.assertEqual(len(context['registrations']), 3)
            
        print("\n=== Test 5: Filter by PPT=yes AND team_size=4 (should show 1 result) ===")
        request = self.factory.get('/dashboard/?has_ppt=yes&team_size=4')
        request.user = self.user
        
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            args, kwargs = mock_render.call_args
            context = args[2]
            
            print(f"Number of results: {len(context['registrations'])}")
            if context['registrations']:
                for i, reg in enumerate(context['registrations']):
                    print(f"Result {i+1}: {reg['team_name']} - Team size: {reg['team_size']} - Has PPT: {reg['has_ppt']}")
            print(f"Context filters: {context['filters']}")
            
            self.assertEqual(len(context['registrations']), 1)
            self.assertEqual(context['registrations'][0]['team_size'], 4)
            self.assertTrue(context['registrations'][0]['has_ppt'])