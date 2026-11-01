#!/usr/bin/env python3
"""Validate a public demo bundle and optionally send it to a generic endpoint."""
import argparse,json,os,urllib.request
from pathlib import Path

def load(path):
    bundle=json.loads(path.read_text(encoding="utf-8"))
    if bundle.get("schema_version")!=1 or not isinstance(bundle.get("questions"),list): raise ValueError("Invalid bundle")
    seen=set()
    for i,q in enumerate(bundle["questions"]):
        required={"year","exam_code","position","statement","alternatives","answer"}
        if required-set(q): raise ValueError(f"Question {i} is incomplete")
        if q["answer"] not in "ABCDE" or set(q["alternatives"])!=set("ABCDE"): raise ValueError(f"Question {i} is invalid")
        key=(q["year"],q["exam_code"],q["position"])
        if key in seen: raise ValueError(f"Duplicate: {key}")
        seen.add(key)
    return bundle["questions"]

def main():
    p=argparse.ArgumentParser();p.add_argument("bundle",type=Path);p.add_argument("--execute",action="store_true");p.add_argument("--batch-size",type=int,default=20);a=p.parse_args();questions=load(a.bundle)
    print(json.dumps({"validated":len(questions),"execute":a.execute}))
    if not a.execute:return
    endpoint=os.environ.get("PIPELINE_IMPORT_ENDPOINT");key=os.environ.get("PIPELINE_IMPORT_API_KEY")
    if not endpoint or not key: raise SystemExit("Configure the example environment variables")
    for start in range(0,len(questions),a.batch_size):
        body=json.dumps({"questions":questions[start:start+a.batch_size]}).encode();request=urllib.request.Request(endpoint,data=body,method="POST",headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"});urllib.request.urlopen(request,timeout=60).read()
if __name__=="__main__": main()
