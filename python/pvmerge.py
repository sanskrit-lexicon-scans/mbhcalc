# coding=utf-8
"""
 pvmerge.py
"""
from __future__ import print_function
import sys, re,codecs
# import json
from make_parvan_verse import init_pagerecs

def init_parvandict(pagerecs):
 d = {}
 for rec in pagerecs:
  parvan = rec.parvan
  assert 1 <= parvan <= 18
  if parvan not in d:
   d[parvan] = []
  recobj = rec.todict()
  d[parvan].append(recobj)
 return d

def merge_verses_version1(pagerecs):
 pvarr = []
 for irec,rec in enumerate(pagerecs):
  if irec == 0:
   pv = [rec.parvan,int(rec.verse1),int(rec.verse2)]
   continue
  rec0 = pagerecs[irec - 1] # previous
  if rec.parvan == rec0.parvan:
   if int(rec.verse1) != (int(rec0.verse2) + 1):
    print('gap: %s: %s,%s  AND %s,%s' %(
     rec.parvan, rec0.verse1,rec0.verse2, rec.verse1,rec.verse2))
    #print(rec0.line)
    #print(rec.line)
    pv.append('gap')
    pvarr.append(pv)
    pv = [rec.parvan,int(rec.verse1),int(rec.verse2),'gap']
   else:
    pv[2] = int(rec.verse2)
  else:
   # new parvan
   pvarr.append(pv)
   pv = [rec.parvan,int(rec.verse1),int(rec.verse2)]
 pvarr.append(pv)
 return pvarr

def write(fileout,pvarr):
 with codecs.open(fileout,"w","utf-8") as f:
  outarr = []
  nvtot = 0
  for pv in pvarr:
   pvstr = [str(x) for x in pv]
   out = ' '.join(pvstr)
   p = pv[0]
   v1 = pv[1]
   v2 = pv[2]
   if v1 > v2:
    out = out + ' ?'
   # outarr.append(out)
   # prepare to update nvtot
   xtra = ''
   if pv[-1] == 'gap':
    xtra = 'nocount'
   elif v1 > v2:
    xtra = 'negcount'
   else:
    nv = (v2 - v1) + 1
    nvtot = nvtot + nv
    xtra = 'nv=%s' % nv
   out = out + ' ' + xtra
   outarr.append(out)
  # add lines for nvtot
  out = 'total verse count (estimate) = %s' % nvtot
  outarr.append(out)
  for out in outarr:
   f.write(out + '\n')
  # check of nvtot
  nvt = 0
  for out in outarr:
   m = re.search(r'nv=([0-9]+)',out)
   if m != None:
    nv = int(m.group(1))
    nvt = nvt + nv
 print(len(pvarr),'lines written to',fileout)
 print(nvtot,'estimated number of verses')
 assert nvtot == nvt
 #print('nvt =',nvt)

def merge_verses(pagerecs):
 pvarr = []
 for irec,rec in enumerate(pagerecs):
  if irec == 0:
   pv = [rec.parvan,int(rec.verse1),int(rec.verse2)]
   continue
  rec0 = pagerecs[irec - 1] # previous
  if rec.parvan == rec0.parvan:
   if int(rec.verse1) != (int(rec0.verse2) + 1):
    pvarr.append(pv)
    # make a gap entry
    p = rec.parvan
    v1 = int(rec0.verse2) + 1
    v2 = int(rec.verse1) - 1
    pvgap = [p,v1,v2,'gap']
    pvarr.append(pvgap)
    # start next one
    pv = [rec.parvan,int(rec.verse1),int(rec.verse2)]
   else:
    pv[2] = int(rec.verse2)
  else:
   # save previous parvan
   pvarr.append(pv)
   # start new parvan
   pv = [rec.parvan,int(rec.verse1),int(rec.verse2)]
   
 pvarr.append(pv)
 return pvarr
  
if __name__ == "__main__":
 filein=sys.argv[1]  # tab-delimited index file
 fileout = sys.argv[2]
 pagerecs = init_pagerecs(filein)
 pvarr = merge_verses(pagerecs)
 write(fileout,pvarr)
 exit(1)
 parvandict = init_parvandict(pagerecs)
 write(fileout,parvandict)
 
