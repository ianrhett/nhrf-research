import re,json,sys
S=sys.argv[1]
D='Plan_to_Play_2026_Update'
def n(s): return re.sub(r'\s+',' ',s).strip()
pages={}
for p in range(1,142):
    pages[p]=[n(open(f'{S}/p2p_{m}/p{p}.txt').read()) for m in ('txt','raw')]
R=[
(12,'land_acquisition','status_claim','Park land acquired since 2017','568.78','acres',None,'Metro Parks','Since 2017, Metro Parks has acquired 568.78','INCONSISTENT: p38 says "More than 500 acres" added since 2017; p113 uses 568 acres.'),
(12,'land_acquisition','status_claim','Acquisition pace vs population growth and 2027 LOS','',None,'2027','Metro Parks','This does not keep up with Nashville’s population growth, nor achieve the','Plan states acquisition since 2017 misses population growth and the recommended 2027 acreage LOS.'),
(12,'funding','funding_estimate','Cost to acquire 2017 recommended land','534','million USD',None,'Metro','P2P 2017 estimated the cost to acquire the recommended 4,540 acres at $534 million.','2017 recommendation: 4,540 acres.'),
(12,'funding','funding_allocated','Metro allocations for park land acquisition since 2017','12.8','million USD',None,'Metro','Since then, a total of $12.8 million has been allocated','From Metro sources; excludes donations and grants (p31 note).'),
(31,'funding','funding_allocated','Share of recommended land acquisition funding allocated 2017 to 2025','2.2','percent','2025','Metro','2.2% of recommended funding for land acquisition allocated 2017 to 2025','$12.8M of $534M.'),
(31,'funding','funding_allocated','Share of recommended facilities funding allocated 2017 to 2025','31.0','percent','2025','Metro','31.0% of recommended funding for facilities capital projects allocated 2017 to 2025','$190M of $611M; contrast with 2.2% for land.'),
(13,'land_acquisition','status_claim','Acquisition near Beaman Park in process','309','acres',None,'Metro Parks','Acquisition of 309 acres near Beaman Park is in process at the time of this printing.','p112: private fundraising ongoing at time of publication.'),
(37,'open_space','baseline','Total Metro Parks acreage (Aug 2025)','15,656.78','acres','2025','Metro Parks','Total Metro Parks Acreage 15,656.78 ac','Inventory as of August 2025.'),
(37,'open_space','baseline','Metro Parks landbank acreage','406.59','acres','2025','Metro Parks','Landbank 406.59 ac',None),
(38,'open_space','status_claim','Acreage LOS change since 2017','21.79 to 21.49','acres per 1,000 residents','2025','Metro Parks','Acreage LOS has decreased from 21.79 acres of park land per 1,000 residents to 21.49 acres per 1,000 residents.','INCONSISTENT: p12 gives the 2017 figure as 21.78; p122 calls 21.49 the "2017 acreage LOS".'),
(46,'habitat_natural_area','status_claim','Natural areas not formally protected','',None,None,'Metro Parks','P2P 2017 noted that most sites in Nashville that are managed in practice as natural areas are not formally protected as such.','Nine years after 2017, designation policy is still "currently developing".'),
(46,'habitat_natural_area','commitment','Designated Natural Area (DNA) policy in development','',None,None,'Metro Parks; Park Board','Metro Parks is currently developing policy that will formally establish designated natural areas (DNAs) within the Metro Parks system.','Protection would be self-imposed by the Park Board, not ordinance.'),
(46,'habitat_natural_area','baseline','Natural areas in Metro Parks','6,500+','acres',None,'Metro Parks','6,500+ ACRES OF NATURAL AREAS IN METRO PARKS','INCONSISTENT: p49 estimates 6,600 acres.'),
(49,'habitat_natural_area','baseline','Park land functionally managed as natural area','6,600 (42%)','acres',None,'Metro Parks','Existing park land that is functionally managed as natural area is estimated at 6,600 acres.','p49 also: 42% of total Metro Parks acreage.'),
(49,'habitat_natural_area','recommendation','DNA target percentage deferred','',None,None,'Metro Parks','Once the DNA program is firmly established and a formal count can be conducted, a target percentage of DNA acres should be established.','No target set; deferred until program exists.'),
(49,'highland_rim_named_place','status_claim','Undeveloped land concentrated on Highland Rim slopes','',None,None,None,'the steep, forested slopes of the Highland Rim in west and northwest Davidson County','Names the Highland Rim as where much remaining undeveloped potential DNA land is concentrated.'),
(49,'policy_mechanism','recommendation','Metro Natural Areas ordinance','',None,None,'Metro Council','Greater protection for natural areas could be achieved by the adoption of a Metro Natural Areas ordinance by the Metro Council.',None),
(47,'highland_rim_named_place','commitment','ECS includes Highland Rim Forest case study','',None,None,'Metro Planning Commission','A Highland Rim Forest case study investigation','Listed in scope of Metro Planning conservation strategy.'),
(51,'funding','recommendation','Reliable land acquisition funding stream','',None,None,'Metro','A commitment to a reliable, predictable funding stream would allow Metro Parks to institutionalize a land acquisition program','p51: acquisition has been reactive to opportunities.'),
(51,'policy_mechanism','status_claim','Greenways Ordinance Conservation Assistance program underfunded','',None,None,'Metro','The existing Greenways Ordinance contains language establishing a Conservation Assistance program that is currently underfunded.',None),
(112,'land_acquisition','target','Tier One new land acquisition','82','acres','2031','Metro Parks','Acquire an estimated 82 acres of additional park, greenway, and','Tier One cost $8M (p112, p114); work plan 2027-2031 (p116).'),
(122,'land_acquisition','target','Tier Two land to hold acreage LOS','507','acres','2031','Metro Parks','Tier Two preserves the 2017 acreage LOS of 21.49 acres per 1,000 residents by adding approximately 507 acres','Tier Two land cost $105.2M (p126, p127); work plan 2027-2031 (p129).'),
(133,'land_acquisition','target','Tier Three land to reach aspirational LOS','1,391','acres','2031','Metro Parks','Acquire approximately 1,391 acres of new land for','Tier Three LOS goal 23.30 acres per 1,000 (p132); land cost $288.75M (p137); work plan 2027-2031 (p139).'),
(132,'open_space','target','Corrected acreage LOS goal for 2027','23.30','acres per 1,000 residents','2027','Metro Parks','Corrected Acreage LOS goal for 2027 for all parkland is 23.30 acres per 1,000 residents',None),
(29,'tree_canopy','status_claim','Trees planted in parks since 2017','6,300+','trees',None,'Metro Parks','Since 2017, more than 6,300 trees have been',None),
]
out=[];bad=[]
for p,cat,it,met,val,unit,ty,rp,ex,note in R:
    ok=any(n(ex) in t for t in pages[p])
    if not ok: bad.append((p,ex))
    out.append([D,p,cat,it,met,val or None,unit,ty,rp,ex,note,'verified' if ok else 'UNVERIFIED',f'PDF p{p}'])
json.dump(out,open(f'{S}/p2p_rows.json','w'),ensure_ascii=False)
print(len(out),'rows; unverified:',bad)
