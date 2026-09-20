import hashlib
import re
from pathlib import Path

def sha256_file(path:str,chunk_size:int=1024*1024)->str:
    digest=hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda:handle.read(chunk_size),b""):
            digest.update(chunk)
    return digest.hexdigest()

def extract_iocs(text:str)->dict[str,list[str]]:
    ips=sorted(set(re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b",text)))
    domains=sorted(set(re.findall(r"\b(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b",text)))
    hashes=sorted(set(re.findall(r"\b[a-fA-F0-9]{32}(?:[a-fA-F0-9]{32}|[a-fA-F0-9]{64})?\b",text)))
    return {"ipv4":ips,"domains":domains,"hashes":hashes}
