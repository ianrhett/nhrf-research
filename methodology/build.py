#!/usr/bin/env python3
import html, os
D=os.path.dirname(os.path.abspath(__file__))
docs=[
("1973","Natural Environmental Analysis","Study","Final","yes","yes"),
("Sep 1981","General Plan for Nashville, 1980-2000","Plan","Adopted","yes","yes"),
("1992","Concept 2010: A General Plan for Nashville-Davidson County","Plan","Adopted","yes","yes"),
("Apr 2006","Ordinance BL2006-1046 (conservation subdivisions in AG and AR2a)","Ordinance","Not enacted","no",""),
("Jun 2009","Green Ribbon Committee Report","Committee report","Advisory","no",""),
("Nov 2009","Green Infrastructure Master Plan","Plan","Final","yes","yes"),
("2010","Tree Canopy Assessment","Study","Final","yes","yes"),
("Mar 2011","Nashville Open Space Plan (Nashville: Naturally)","Plan","Final","yes","yes"),
("Jan 2013","Unified Flood Preparedness Plan","Plan","Final","yes","no"),
("2013","NashvilleNext Background Report: Natural Resources and Green Spaces","Background report","Background","no",""),
("Jan 2014","Home Buyout Program Internal Audit (Metro Water Services)","Report","Final","yes","yes"),
("Jun 2015","NashvilleNext: A General Plan (Volumes I to IV, 17 files)","Plan","Adopted; amended Aug 2017","yes","yes"),
("Jun 2015","Planning Commission minutes, June 22, 2015","Minutes","Final","yes","no"),
("Apr 2016","Planning Commission minutes, April 28, 2016","Minutes","Final","yes","no"),
("May 2016","Planning Commission minutes, May 26, 2016","Minutes","Final","yes","no"),
("2016","Urban Forestry and Landscape Master Plan","Plan","Final; not adopted","yes","yes"),
("Mar 2017","Plan to Play: Parks and Greenways Master Plan","Plan","Final","yes","yes"),
("Jun 2017","Ordinance BL2017-725 (Conservation Assistance Grant Fund)","Ordinance","Enacted","yes","no"),
("2017","Livable Nashville","Plan","Draft","no",""),
("Dec 2019","MS4 Annual Report FY19 (Metro Water Services)","Report","Final","yes","yes"),
("2021","Sustainability Advisory Committee Climate Mitigation Action Plan","Committee report","Advisory","no",""),
("Aug 2021","Ordinance BL2021-829 (tree protection on Metro properties)","Ordinance","Enacted","yes","no"),
("Apr 2022","Planning Commission minutes, April 28, 2022","Minutes","Final","yes","no"),
("Dec 2023","Urban Tree Canopy Assessment","Study","Final","yes","yes"),
("Apr 2024","Executive Order 41 (Amended): Tree Policy","Executive order","Issued","yes","no"),
("Sep 2024","Climate Adaptation and Resilience Plan","Plan","Final","yes","yes"),
("Jun 2025","Stormwater Master Plan","Plan","Draft","no",""),
("Oct 2025","Resolution RS2025-1549 (recognizing the Highland Rim Forest)","Resolution","Adopted","yes","no"),
("Oct 2025","Resolution RS2025-1556 (Beaman Park grant application)","Resolution","Adopted","yes","no"),
("Mar 2026","Davidson County Ecological Conservation Strategy (project page)","Web page","In progress","yes","no"),
("Apr 2026","Multi-Hazard Mitigation Plan","Plan","Adopted; FEMA approved","yes","yes"),
("Jun 2026","Plan to Play 2026 Update (with Appendix, 2 files)","Plan","Approved by Park Board","yes","yes"),
("Jul 2026","Mayor's release: Beaman Park acquisition","Media release","Issued","yes","no"),
("Sep 2026","Parks Board meeting agenda, September 1, 2026","Agenda","Final","yes","no"),
("2022","Metro Code 17.28.030, Hillside development standards","Code","In force; last amended 2022","yes","no"),
("2025","Metro Code 17.28.065, Trees","Code","In force; last amended 2025","yes","no"),
("2022","Metro Code 17.40.440, Tree protection and replacement","Code","In force; last amended 2022","yes","no"),
("Jun 2024","Subdivision Regulations Chapter 4 (Rural Character Subdivisions)","Regulation","Adopted; amended June 2024","yes","no"),
]
assert len(docs)==38 and sum(d[4]=="yes" for d in docs)==32 and sum(d[5]=="yes" for d in docs)==15
rows="\n".join(f'<tr class="{"" if d[4]=="yes" else "unc"}"><td>{html.escape(d[0])}</td><td>{html.escape(d[1])}</td><td>{d[2]}</td><td>{html.escape(d[3])}</td><td class="c">{"Yes" if d[4]=="yes" else "No"}</td><td class="c">{"Yes" if d[5]=="yes" else ("" if d[4]=="no" else "No")}</td></tr>' for d in docs)
steps=[("32","documents","We gathered Metro's documents","Adopted plans, studies and reports from 1973 to 2026, plus the laws, code and minutes that show what Metro actually did."),
("1,272","statements","We read them and copied out every statement","Every statement about forests, trees, open space and steep slopes, word for word, with its page number."),
("340","forest recommendations","We kept the ones that ask Metro to act","Recommendations, commitments, targets and cost estimates for the forest, found in 15 documents."),
("19","recommendations, made 216 times","We grouped the ones that ask for the same thing","The same request in different words counts once as a recommendation and each time as a mention."),
("7","enacted rules","We looked for what was actually done","Ordinances, code, executive orders, budgets and minutes: proof of action, not more plans."),
("1 of 19","fully implemented","We scored each recommendation","1 fully implemented, 15 carried out in part, 3 with no implementation reported.")]
W=640;H=74*6+10;svg=[f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="Six steps from 32 documents to 1 of 19 recommendations fully implemented">']
for i,(n,u,t,d) in enumerate(steps):
    y=8+i*74; w=W-i*52; x=(W-w)/2; fill="#1f4d36" if i<5 else "#b3261e"
    op=1-i*0.1 if i<5 else 1
    svg.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="62" rx="6" fill="{fill}" fill-opacity="{op:.2f}"/>')
    svg.append(f'<text x="{x+16:.0f}" y="{y+40}" font-size="27" font-weight="700" fill="#fff" font-family="Helvetica Neue,Helvetica,Arial,sans-serif">{html.escape(n)}</text>')
    tx=x+16+ (len(n)*16+18)
    svg.append(f'<text x="{tx:.0f}" y="{y+25}" font-size="13" font-weight="700" fill="#fff" font-family="Helvetica Neue,Helvetica,Arial,sans-serif">{i+1}. {html.escape(t)}</text>')
    svg.append(f'<text x="{tx:.0f}" y="{y+45}" font-size="11" fill="#e7efe9" font-family="Helvetica Neue,Helvetica,Arial,sans-serif">{html.escape(u)}</text>')
svg.append('</svg>')
desc="".join(f'<li><b>{i+1}. {html.escape(t)}.</b> {html.escape(d)}</li>' for i,(n,u,t,d) in enumerate(steps))
tpl=open(os.path.join(D,'methodology.tmpl.html')).read()
open(os.path.join(D,'methodology.html'),'w').write(tpl.replace('{{FUNNEL}}',"\n".join(svg)).replace('{{STEPS}}',desc).replace('{{ROWS}}',rows))
print('ok')
