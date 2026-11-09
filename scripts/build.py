from pathlib import Path
import hashlib, json, shutil
root=Path(__file__).resolve().parent.parent
output=root/'_site'
if output.exists(): shutil.rmtree(output)
shutil.copytree(root/'site',output)
for video in json.loads((root/'video-parts/manifest.json').read_text()):
    destination=output/video['path']
    destination.parent.mkdir(parents=True,exist_ok=True)
    digest=hashlib.sha256()
    with destination.open('wb') as stream:
        for part in video['parts']:
            data=(root/'video-parts'/part).read_bytes()
            stream.write(data)
            digest.update(data)
    if digest.hexdigest()!=video['sha256']: raise RuntimeError('Incomplete video: '+video['path'])
(output/'.nojekyll').touch()
print('Site ready:',output)
