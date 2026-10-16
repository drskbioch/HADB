"""Build dist/backend_bundle.zip: backend code, hadb.sqlite, downloads/, docker-compose.yml, nginx.conf, .env.example, Dockerfile, requirements.txt, openapi.json, DEPLOY_GUIDE.md.
No secrets, no .env, no certificates, no record-level GBIF data, no tests."""
import hashlib, zipfile
from pathlib import Path
R = Path(__file__).resolve().parents[1]; B = R / 'backend'; out = R / 'dist' / 'backend_bundle.zip'; out.parent.mkdir(exist_ok=True)
files = [(B / 'app' / 'main.py', 'app/main.py'), (B / 'app' / '__init__.py', 'app/__init__.py'), (B / 'requirements.txt', 'requirements.txt'), (B / 'Dockerfile', 'Dockerfile'), (B / 'docker-compose.yml', 'docker-compose.yml'), (B / 'nginx.conf', 'nginx.conf'),
         (B / '.env.example', '.env.example'), (B / 'openapi.json', 'openapi.json'), (B / 'data' / 'hadb.sqlite', 'data/hadb.sqlite'), (R / 'DEPLOY_GUIDE.md', 'DEPLOY_GUIDE.md')]
files += [(p, 'data/downloads/' + p.name) for p in sorted((B / 'data' / 'downloads').iterdir()) if p.is_file()]
lines = []
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for src, arc in files:
        z.write(src, arc); lines.append('%s  %d  %s' % (hashlib.sha256(src.read_bytes()).hexdigest().upper(), src.stat().st_size, arc))
    z.writestr('certs/README.txt', 'Put fullchain.pem and privkey.pem here on the server (see DEPLOY.md, section 3, step 6). Never commit or ship them.\n')
    z.writestr('certbot-webroot/README.txt', 'Webroot for the optional certbot --webroot challenge.\n')
    z.writestr('BUNDLE_MANIFEST.txt', 'SHA256  bytes  path\n' + '\n'.join(lines) + '\n')
print('dist/backend_bundle.zip', out.stat().st_size, 'bytes,', len(files) + 3, 'entries')
