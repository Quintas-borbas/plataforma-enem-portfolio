#!/usr/bin/env python3
"""Extract and validate ENEM items from official INEP microdata."""
import argparse,csv,json,re
from pathlib import Path

def clean(value):
    return re.sub(r"\s+"," ",value or "").strip() or None

def main():
    p=argparse.ArgumentParser();p.add_argument("--items",type=Path,required=True);p.add_argument("--year",type=int,required=True);p.add_argument("--area",required=True);p.add_argument("--exam-code");p.add_argument("--output",type=Path,required=True);a=p.parse_args()
    accepted=[];review=[];seen=set()
    with a.items.open(encoding="latin1",newline="") as stream:
        reader=csv.DictReader(stream,delimiter=";")
        required={"CO_POSICAO","CO_PROVA","SG_AREA","TX_GABARITO"}
        missing=required-set(reader.fieldnames or [])
        if missing: raise SystemExit(f"Missing columns: {sorted(missing)}")
        for row in reader:
            if clean(row.get("SG_AREA"))!=a.area or (a.exam_code and clean(row.get("CO_PROVA"))!=a.exam_code): continue
            key=(a.year,clean(row.get("CO_PROVA")),int(row["CO_POSICAO"]))
            if key in seen: raise SystemExit(f"Duplicate identity: {key}")
            seen.add(key)
            alternatives={letter:clean(row.get(f"TX_ALTERNATIVA_{letter}") or row.get(f"DESC_ALTER_{letter}")) for letter in "ABCDE"}
            question={"year":a.year,"exam_code":key[1],"position":key[2],"area":a.area,"statement":clean(row.get("TX_ENUNCIADO") or row.get("DESC_ENUNCIADO")),"alternatives":alternatives,"answer":clean(row.get("TX_GABARITO")),"classification":{"discipline":"TODO","subject":"TODO","confidence":None,"reviewed":False}}
            reasons=[]
            if question["answer"] not in "ABCDE": reasons.append("invalid_answer")
            if not question["statement"]: reasons.append("missing_statement")
            if any(not v for v in alternatives.values()): reasons.append("missing_alternative")
            (review if reasons else accepted).append({"identity":key,"reasons":reasons} if reasons else question)
    bundle={"schema_version":1,"source":"official_inep_microdata","questions":accepted,"review":review}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"validated":len(accepted),"review":len(review)}))
if __name__=="__main__": main()
