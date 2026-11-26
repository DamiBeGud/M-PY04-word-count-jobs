# word-count-jobs

Native Python3.11–3.13 application; intended acceptance runtime3.12.
Install `python -m pip install -r requirements.txt` in an isolated environment.
Run `python -m pytest`. Start `uvicorn word_count_jobs.app:app --host 0.0.0.0 --port 8204`.

Requires CELERY_BROKER_URL, CELERY_RESULT_BACKEND and unique QUEUE_NAMESPACE. Start the separate native worker `celery -A word_count_jobs.worker.celery worker --loglevel=warning --concurrency=1`. Broker/result key prefixes and queue routes are namespaced; this is controlled state separation, not a security boundary. No eager mode or FLUSH operation is provided.

Set `API_TOKEN` through a private runtime Secret reference. Job submission and result reads require a Bearer token. Health routes remain available for probes.

POST /jobs {reference,text} returns202/job_id; GET /jobs/:uuid returns same-job state/result. Worker output preserves reference. Liveness /health/live does not establish task processing.
Tests are source-native development checks. Queue/result calls are simulated; actual Redis and native worker acceptance is separate.
AI-assisted researcher-created source; no deployment files or runtime credentials.
