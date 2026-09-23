from unittest.mock import Mock
import pytest




def fetch_user_data(api_client):
    try:
        return api_client.get_user()
    except ConnectionError:
        return "Fallback User"

def test_fetch_user_data_handles_error():
    mock_api = Mock()
    # Der Mock wirft nun einen Fehler, anstatt einen Wert zurückzugeben
    mock_api.get_user.side_effect = ConnectionError("API offline")
    
    result = fetch_user_data(mock_api)
    
    assert result == "Fallback User"