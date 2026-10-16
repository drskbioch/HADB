"""Write backend/openapi.json from the app."""
import json, sys
from pathlib import Path
B = Path(__file__).resolve().parent; sys.path.insert(0, str(B))
from app.main import app
(B / 'openapi.json').write_text(json.dumps(app.openapi(), indent=1), encoding='utf-8'); print('openapi.json', len(app.openapi()['paths']), 'paths')
