# gate-demo-backend

Minimal Python backend for the review-gate greeting demo.

## Prerequisites

- Python 3.8 or newer (no third-party packages required)

## Start

From this directory, run:

```sh
python3 server.py
```

The backend listens at `http://127.0.0.1:8001`. It accepts `POST /greet` with
JSON containing a string `name`, and allows browser requests from
`http://127.0.0.1:8000`.

## Check

With the backend running, send:

```sh
curl -i -X POST http://127.0.0.1:8001/greet \
  -H 'Content-Type: application/json' \
  -d '{"name":"Ada"}'
```

The response is HTTP 200 with `Content-Type: application/json` and body:

```json
{"greeting": "Hello, Ada!"}
```
