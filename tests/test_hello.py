def test_hello(client):
    assert client.get('/api/v1').status_code == 200
    assert client.post('/api/v1').status_code == 405
    assert client.put('/api/v1').status_code == 405
    assert client.delete('/api/v1').status_code == 405
