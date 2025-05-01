import unittest
from unittest.mock import patch, MagicMock, mock_open
from main import load_config, extract_domain, check_health, log_result


class TestMonitorScript(unittest.TestCase):

    # Test for loading configuration from YAML file
    def test_load_config(self):
        # Mock a sample YAML configuration with the required fields
        sample_config = """
        - url: "https://example.com/endpoint"
          method: "POST"
          body: '{"key":"value"}'
          headers:
            content-type: application/json
          name: "Test endpoint 1"
        - url: "https://example.com/"
          method: "GET"
          name: "Test endpoint 2"
        - url: "https://example.com/another"
          method: "POST"
          body: '{"data":"info"}'
          headers:
            content-type: application/json
          name: "Test endpoint 3"
        - url: "https://example.com/error"
          method: "GET"
          name: "Test endpoint 4"
        """
        with patch("builtins.open", unittest.mock.mock_open(read_data=sample_config)):
            config = load_config("fake_config.yaml")
            self.assertEqual(len(config), 4)
            self.assertEqual(config[0]['url'], 'https://example.com/endpoint')
            self.assertEqual(config[0]['name'], 'Test endpoint 1')
            self.assertEqual(config[0]['method'], 'POST')
            self.assertEqual(config[0]['body'], '{"key":"value"}')
            self.assertEqual(config[0]['headers'], {'content-type': 'application/json'})

    # Test domain extraction from URL
    def test_extract_domain(self):
        url = "https://example.com/endpoint"
        domain = extract_domain(url)
        self.assertEqual(domain, "example.com")

    # Mock the request function for testing
    @patch('requests.request')
    def test_check_health_up(self, mock_request):
        # Simulate a successful response (status code 200, response time under 500ms)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        result = check_health({
            'url': 'https://example.com/',
            'method': 'GET',
            'name': 'Test endpoint 2'
        })
        self.assertEqual(result, "UP")

    @patch('requests.request')
    def test_check_health_down(self, mock_request):
        # Simulate a failed response (status code 500, response time above 500ms)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_request.return_value = mock_response

        result = check_health({
            'url': 'https://example.com/error',
            'method': 'GET',
            'name': 'Test endpoint 4'
        })
        self.assertEqual(result, "DOWN")

    # Test logging function
    @patch("builtins.open", unittest.mock.mock_open())
    def test_log_result(self):
        domain_stats = {
            'example.com': {'up': 3, 'total': 4},
            'another.com': {'up': 2, 'total': 3},  # Availability 66%
        }

        with patch("builtins.open", mock_open()) as mocked_open_func:
            log_result(domain_stats)
            mock_file_handle = mocked_open_func()

            mock_file_handle.write.assert_any_call('example.com has 75% availability percentage\n')


if __name__ == '__main__':
    unittest.main()
