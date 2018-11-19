
def test_index(client):
    resp = client.get('/')
    assert resp.status_code == 302
    assert '/apidocs' in resp.location
