import re
import base64
import os
import hashlib

html_path = "index.html"
img_dir = "./assets/img"
os.makedirs(img_dir, exist_ok=True)

with open(html_path, "r", encoding="utf-8", errors="replace") as f:
    html = f.read()

# content hash → 저장된 파일명 (중복 제거)
hash_to_filename = {}
counter = 1

def replace_match(m):
    global counter
    mime = m.group(1)   # jpeg / png / gif 등
    data = m.group(2)

    ext = mime if mime != "jpeg" else "jpg"
    digest = hashlib.md5(data.encode()).hexdigest()

    if digest in hash_to_filename:
        filename = hash_to_filename[digest]
    else:
        filename = f"image_{counter:02d}.{ext}"
        counter += 1
        filepath = os.path.join(img_dir, filename)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(data))
        hash_to_filename[digest] = filename
        print(f"  저장: {filepath}")

    web_path = f"{img_dir}/{filename}".replace("\\", "/")
    return f'src="{web_path}"'

pattern = r'src="data:image/([^;]+);base64,([^"]+)"'
new_html, n = re.subn(pattern, replace_match, html)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"\n완료: {n}개 교체, {len(hash_to_filename)}개 파일 저장")
