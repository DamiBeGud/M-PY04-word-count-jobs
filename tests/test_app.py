from types import SimpleNamespace
from unittest.mock import patch
from fastapi.testclient import TestClient
from word_count_jobs.app import app
from word_count_jobs.worker import transform,celery
client=TestClient(app);headers={'Authorization':'Bearer synthetic-unit-token'}
def test_transformation_and_namespace():
    result=transform('unit-one',"One one TWO")
    assert result=={"reference":"unit-one","counts":{"one":2,"two":1}}
    assert celery.conf.broker_transport_options['global_keyprefix']=='synthetic-unit:'
    assert celery.conf.result_backend_transport_options['global_keyprefix']=='synthetic-unit:'
def test_http_with_simulated_queue():
    job='3af6507c-5ed0-4913-91af-f570b07352e1'
    with patch('word_count_jobs.app.process.apply_async',return_value=SimpleNamespace(id=job)):
        assert client.post('/jobs',json={'reference':'unit-one','text':'one'},headers=headers).status_code==202
    with patch('word_count_jobs.app.celery.AsyncResult',return_value=SimpleNamespace(state='SUCCESS',result=transform('unit-one','one'))):
        assert client.get('/jobs/'+job,headers=headers).json()['result']['reference']=='unit-one'
    assert client.get("/jobs/not-uuid").status_code==422
