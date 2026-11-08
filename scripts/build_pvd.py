import csv, io, sys
src, out = sys.argv[1], sys.argv[2]
rows = list(csv.reader(open(src, newline='', encoding='utf-8')))
def dump(rs):
    b = io.StringIO(); csv.writer(b, lineterminator='\r\n').writerows(rs); return b.getvalue()
assert dump(rows) == open(src, newline='', encoding='utf-8').read(), "round-trip mismatch"
hdr, body, foot = rows[0], rows[1:-1], rows[-1]
assert [r[0] for r in body] == [str(i) for i in range(1, 21)], "unexpected pair numbering"
H = {h: i for i, h in enumerate(hdr)}
def row(**kw):
    r = [''] * len(hdr)
    for k, v in kw.items(): r[H[k]] = v
    return r
p13 = body[12]
assert p13[H['theme']] == 'Conservation subdivision'
p13[H['delivered_doc']] = 'MPC_Minutes_2022-04-28'
p13[H['delivered_page']] = '13'
p13[H['reported_2026']] = 'BL2022-1121 (2022) created Conservation Development, required when 10% of a site has natural features; 20% preservation threshold. No 50% open space and no by-right conservation subdivision.'
p13[H['assessment']] = 'Not met'
p13[H['notes']] = 'An earlier conservation subdivision bill (BL2006-1046, 50% open space) was deferred indefinitely Aug 15, 2006 and withdrawn Aug 21, 2007. See pair 22 and docs/research/ENACTMENT-CHECKS.md.'
body.append(row(pair='21', theme='Hillside regulation', promise_doc='NashvilleNext_Vol4_Actions', promise_page='69',
    promise='NR 1.1 #210: Strengthen hillside development regulations to minimize development on greater than 15% slopes.',
    promised_value='15', unit='percent slope', due='2018',
    delivered_doc='Metro_Code_17.28.030', delivered_page='history note',
    reported_2026='Residential grading and clearing limits still start at 20% slopes; lots under one acre preserve slopes of 25% or more; lots of one acre or more are exempt. Three amendments since 2015 (BL2015-1153, BL2019-111, BL2022-1121); none lowers the residential threshold to 15%.',
    assessment='Not met',
    notes='Near term (1-3 years) from 2015 adoption, Metro Planning. BL2015-1153 added alternative (-A) district names; BL2019-111 added no-STRP (-NS) district names; BL2022-1121 sent subdivisions on 20%+ slopes to Conservation Development (MPC minutes 2022-04-28 p18). The 15% figure applies only to nonresidential ISR adjustments, which predate 2015. Code read on Municode 2026-10-22.'))
body.append(row(pair='22', theme='Conservation subdivision', promise_doc='NashvilleNext_Vol4_Actions', promise_page='72',
    promise='NR 1.4 #182: Enact a conservation subdivision ordinance by right with a minimum of 50% open space requirement.',
    promised_value='50', unit='percent open space (minimum)', due='2021',
    delivered_doc='MPC_Minutes_2022-04-28', delivered_page='13; 14; 16',
    reported_2026='BL2022-1121 (Council third reading May 17, 2022) replaced the Cluster Lot Option with Conservation Development: required on R and RS subdivisions where at least 10% of the site has listed natural features, with a 20% preservation threshold.',
    delivered_value='20', pct_delivered='=IFERROR(L23/F23,"")', assessment='Not met',
    notes='Mid term printed 4-6 years (Vol IV p4 defines 4 to 7). Delivered tool is required, not by right, and sets 20% rather than 50%. Pct is the threshold ratio, not acres. Same ask as pair 13 (2011, due 2012). Related #174 (cluster lots to 33% preserved land): the Cluster Lot Option was removed from the code in 2022 (Metro Planning, Compact Development open house page). BL2006-1046 had defined a 50% conservation subdivision and was withdrawn in 2007.'))
assert len(body) == 22
open(out, 'w', newline='', encoding='utf-8').write(dump([hdr] + body + [foot]))
