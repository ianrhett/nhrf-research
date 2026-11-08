import re,json,sys
S=sys.argv[1]
n=lambda s:re.sub(r'\s+',' ',s).strip()
D='Hazard_Mitigation_Plan_2026_Final'
R=[
(17,'forest_protection','baseline','Steep forested slopes function as headwaters',None,None,None,None,'In addition to providing wildlife habitat, steeply sloping areas with mature forests are important headwater areas, slowing down and absorbing water runoff and filtering water to improve water quality.','Plan links steep forested slopes to runoff control; flooding is its top-ranked hazard (p71).'),
(134,'highland_rim_named_place','baseline','Landslides on slopes adjacent to Highland Rim escarpment',None,None,None,None,'Landslides have occurred in this area due to construction-altered colluvium soils on steep slopes adjacent to the Highland Rim escarpment.','Hazard profile; repeated in capability assessment p301 followed by CPT decision not to add regulation.'),
(65,'floodplain_stream','status_claim','Flooding in top three hazards every assessment year',None,None,None,'Metro OEM; CPT','Flooding, tornadoes, and winter storms have consistently ranked as Davidson County’s top three hazards across all assessment years.','Assessment years charted: 2012, 2014, 2019, 2023, 2025 (Figure 40-3, p70).'),
(71,'floodplain_stream','baseline','Top-ranked hazard in Davidson County (2025 HIRA)','1','rank','2025','Metro OEM; CPT','Based on this most recent assessment (2025), the top 5 hazards for all of Davidson County are:','Order as printed: Flooding, Tornado, Winter Storm, Extreme Temperatures (Heat/Cold), Communicable Diseases.'),
(71,'floodplain_stream','baseline','Flooding risk factor score (Table 40-3)','167.2','risk factor','2025','Metro OEM; CPT','Flooding','Table 40-3 HIRA Total Risk Scores: Flooding 167.2 (1st of 15); Tornado 156.5; Winter Storm 145.0. verified_by_hand: table values read from extracted table text.'),
(71,'forest_protection','baseline','Wildfire risk factor score (Table 40-3)','88.7','risk factor','2025','Metro OEM; CPT','Wildfire','Table 40-3: 11th of 15 hazards. verified_by_hand: table values read from extracted table text.'),
(71,'forest_protection','baseline','Landslide/Sinkhole risk factor score (Table 40-3)','80.8','risk factor','2025','Metro OEM; CPT','Landslide/Sinkhole','Table 40-3: 14th of 15 hazards; context for p301 decision not to regulate steep slopes. verified_by_hand: table values read from extracted table text.'),
]
out=[];bad=[]
for p,c,i,m,v,u,t,rp,ex,note in R:
    txt=n(open(f'{S}/hmp_txt/p{p}.txt').read())
    ok=n(ex) in txt
    if p==71 and i=='baseline' and ex in('Flooding','Wildfire','Landslide/Sinkhole'):
        ok=ok and v in txt
    if not ok: bad.append((p,ex))
    tag='verified_by_hand' if 'verified_by_hand' in (note or '') else 'verified'
    out.append([D,p,c,i,m,v,u,t,rp,ex,note,tag,f'PDF p{p}'])
print(json.dumps(out,ensure_ascii=False)); print('BAD',bad,file=sys.stderr)
