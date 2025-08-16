import json
from app.main import app

def test_health():
	client = app.test_client()
	resp = client.get('/api/health')
	assert resp.status_code == 200
	data = resp.get_json()
	assert data['status'] == 'ok'


def test_process_text_minimal():
	client = app.test_client()
	payload = {"text": "Photosynthesis converts light energy into chemical energy in plants."}
	resp = client.post('/api/process-text', data=json.dumps(payload), content_type='application/json')
	assert resp.status_code == 200
	data = resp.get_json()
	assert 'summary' in data
	assert isinstance(data.get('highlights'), list)
	assert isinstance(data.get('quiz'), list)