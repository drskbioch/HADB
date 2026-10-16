"""Vercel entry point: exposes the FastAPI app (backend/app/main.py) as a serverless function. vercel.json rewrites every path here.

TEMPORARY DIAGNOSTIC: GET /api/index returns what the function receives, to find out which path FastAPI sees behind the rewrite.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.main import app as _fastapi  # noqa: E402


class Entry:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http' and scope['path'] == '/api/index':
            body = json.dumps({'path': scope['path'], 'raw_path': (scope.get('raw_path') or b'').decode(), 'query': scope['query_string'].decode(),
                               'root_path': scope.get('root_path'), 'headers': {k.decode(): v.decode() for k, v in scope['headers']}}, indent=1).encode()
            await send({'type': 'http.response.start', 'status': 200, 'headers': [(b'content-type', b'application/json')]})
            await send({'type': 'http.response.body', 'body': body})
            return
        await self.inner(scope, receive, send)


app = Entry(_fastapi)
