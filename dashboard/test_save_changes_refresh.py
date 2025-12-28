import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

class TestSaveChangesRefresh(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    @patch('dashboard.views.get_supabase_client')
    def test_update_selection_status_endpoint(self, mock_get_supabase):
        """Test that the update selection status endpoint works correctly"""
        # Mock Supabase response
        mock_supabase = MagicMock()
        mock_get_supabase.return_value = mock_supabase
        
        # Mock successful update response
        mock_response = MagicMock()
        mock_response.data = {'success': True}
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response
        
        # Create POST request
        request = self.factory.post(
            reverse('update_selection_status'),
            data=json.dumps({
                'registration_id': 1,
                'selection_status': 'selected'
            }),
            content_type='application/json'
        )
        request.user = self.user
        request.META['HTTP_X_CSRFTOKEN'] = 'test-csrf-token'
        
        # Import the view
        from dashboard.views import update_selection_status_view
        
        # Get response
        response = update_selection_status_view(request)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_html_contains_refresh_logic(self):
        """Test that the HTML template contains the refresh logic"""
        # Login the user
        self.client.login(username='testuser', password='testpass123')
        
        # Mock the dashboard view to return a simple response
        with patch('dashboard.views.get_supabase_client'):
            response = self.client.get(reverse('dashboard'))
            
            # Check that the response contains the refresh JavaScript
            self.assertContains(response, 'location.reload()')
            self.assertContains(response, 'setTimeout')
            self.assertContains(response, '1500')  # 1.5 second delay