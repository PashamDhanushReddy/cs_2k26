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
    def test_team_members_json_in_context(self, mock_get_supabase):
        # Mock Supabase response
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock data
        mock_data = [{
            'id': 1,
            'team_name': 'Test Team',
            'member1_name': 'Leader',
            'member1_email': 'leader@test.com',
            'member1_phone': '1234567890',
            'member1_roll': 'R1',
            'is_leader1': True,
            'member2_name': 'Member',
            'member2_email': 'member@test.com',
            'member2_phone': '0987654321',
            'member2_roll': 'R2',
            'is_leader2': False,
            # Add other required fields to avoid key errors if any
            'college': 'Test College',
            'college_code': 'TC',
            'registration_date': '2023-01-01T12:00:00',
            'selection_status': 'pending',
        }]
        
        # Setup chain: table().select().execute() and other calls
        mock_query = MagicMock()
        mock_supabase.table.return_value = mock_query
        mock_query.select.return_value = mock_query
        mock_query.ilike.return_value = mock_query
        mock_query.eq.return_value = mock_query
        mock_query.gte.return_value = mock_query
        mock_query.lte.return_value = mock_query
        
        # Mock execute() response for the main query
        mock_response = MagicMock()
        mock_response.data = mock_data
        mock_query.execute.return_value = mock_response

        # Create request
        request = self.factory.get('/dashboard/')
        request.user = self.user

        # Get response
        with patch('dashboard.views.render') as mock_render:
            dashboard_view(request)
            
            # Get the context passed to render
            args, kwargs = mock_render.call_args
            context = args[2]
            
            # Check registrations
            registrations = context['registrations']
            self.assertEqual(len(registrations), 1)
            reg = registrations[0]
            
            # Check team_members_json
            self.assertIn('team_members_json', reg)
            
            # Parse the JSON to verify it
            team_members = json.loads(reg['team_members_json'])
            self.assertEqual(len(team_members), 2)
            
            self.assertEqual(team_members[0]['name'], 'Leader')
            self.assertEqual(team_members[0]['roll'], 'R1')
            self.assertEqual(team_members[0]['is_leader'], True)
            
            self.assertEqual(team_members[1]['name'], 'Member')
            self.assertEqual(team_members[1]['roll'], 'R2')
            self.assertEqual(team_members[1]['is_leader'], False)
