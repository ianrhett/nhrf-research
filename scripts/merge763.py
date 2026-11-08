import openpyxl,json,re,sys
S=sys.argv[1]; ADD=sys.argv[2]
n=lambda s:re.sub(r'\W+',' ',str(s or '')).lower().strip()
wb=openpyxl.load_workbook(f'{S}/wb/base.xlsx')
C=wb['Commitments']
ex=[list(r) for r in C.iter_rows(min_row=2,values_only=True) if r[0]]
def dup(r):
    for e in ex:
        if e[0]!=r[0]: continue
        a,b=n(e[9]),n(r[9])
        if not a or not b: continue
        if len(b)<25:
            if str(e[1])==str(r[1]) and n(e[4])==n(r[4]): return e
            continue
        if a in b or b in a: return e
        if str(e[1])==str(r[1]) and str(e[5] or '')==str(r[5] or '') and r[5] and n(e[6])==n(r[6]): return e
    return None
add=openpyxl.load_workbook(ADD,read_only=True)
A=[list(r) for r in add['Commitments'].iter_rows(min_row=2,values_only=True) if r[0]]
P=json.load(open(f'{S}/p2p_rows.json')); H=json.load(open(f'{S}/hmp_add.json'))
new=[];skipped=[]
for grp,rows in (('additions',A),('p2p',P),('hmp',H)):
    for r in rows:
        d=dup(r)
        if d: skipped.append((grp,r[1],r[4],'~',d[4])); continue
        new.append(r); ex.append(r)
for r in new: C.append(r)
for r in new:
    if r[2]=='highland_rim_named_place': wb['Highland Rim & named places'].append(r[:12])
    if str(r[10] or '').startswith('INCONSISTENT'): wb['Inconsistencies'].append(r[:12])
ms=wb['Sources']
rows=[[c.value for c in r] for r in ms.iter_rows()]
have={r[0] for r in rows}
tot=next(i for i,r in enumerate(rows,1) if r[0]=='Total')
srcs=[list(r) for r in add['Sources'].iter_rows(min_row=2,values_only=True) if r[0] and r[0] not in have and ' ' not in str(r[0])]
if srcs:
    ms.insert_rows(tot,len(srcs))
    for k,s in enumerate(srcs):
        for j,v in enumerate(s[:6],1): ms.cell(tot+k,j,v)
tr=tot+len(srcs)
for r in range(2,tr): ms.cell(r,7,f'=COUNTIF(Commitments!$A:$A,A{r})')
ms.cell(tr,7,f'=SUM(G2:G{tr-1})')
B='https://www.nashvillehighlandrimforest.org/archive/'
for r in range(2,tr):
    d=ms.cell(r,1).value
    if d=='Hazard_Mitigation_Plan_2026_Final':
        ms.cell(r,3,"April 2026; adopted by Mayor O'Connell April 15, 2026; FEMA approved June 4, 2026"); ms.cell(r,4,'Final; FEMA approved (https://www.nashville.gov/departments/emergency-management/planning)')
    if d=='NEA_1973_Natural_Environmental_Analysis': ms.cell(r,6,B+'PlanningCommissionNaturalEnvironmentalAnalysis1973.pdf')
    if d=='General_Plan_1980_2000': ms.cell(r,6,B+'GP1980-2000.pdf')
for r in range(tr+1,ms.max_row+1):
    v=ms.cell(r,1).value
    if v and 'verify column' in str(v) and 'verified_ocr' not in str(v):
        ms.cell(r,1,str(v)+' "verified_ocr" = matched against Tesseract OCR of an archival scan (1973 NEA, 1980 General Plan).')
out=f'{S}/wb/NHRF_Commitments.xlsx'; wb.save(out)
from collections import Counter
print('added',len(new),Counter(r[0] for r in new)); print('skipped',len(skipped))
for s in skipped: print(' ',s)
print('rows now',sum(1 for r in openpyxl.load_workbook(out,read_only=True)['Commitments'].iter_rows(min_row=2,values_only=True) if r[0]))
print('sources added',[s[0] for s in srcs])
