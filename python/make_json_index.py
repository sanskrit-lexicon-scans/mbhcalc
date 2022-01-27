# coding=utf-8
from __future__ import print_function
import sys, re,codecs
import json

class Pagerec(object):
 def __init__(self,line,iline):
  line = line.rstrip('\r\n')
  parts = line.split('\t')
  assert len(parts) == 6
  self.line = line
  self.iline = iline
  self.vol = parts[0]
  self.page = parts[1]
  self.parvan_roman = parts[2]
  self.verse1 = parts[3]
  self.verse2 = parts[4]
  self.numverse = parts[5]
  self.parvan = self.parse_parvan_roman()
 def parse_parvan_roman(self):
  x = self.parvan_roman
  rmap = {
   'I':1, 'II':2, 'III':3, 'IV':4, 'V':5,
    'VI':6, 'VII':7, 'VIII':8, 'IX':9, 'X':10,
    'XI':11, 'XII':12, 'XIII':13, 'XIV':14, 'XV':15,
    'XVI':16, 'XVII':17, 'XVIII':18, '--':None}
  if x not in rmap:
   print('error at line',self.iline + 1)
   exit(1)
  y = rmap[x]
  return y
 def todict(self):
  e = {
   'v':self.vol, 'page':int(self.page), 'p':int(self.parvan),
   'v1':int(self.verse1), 'v2':int(self.verse2), 'n':int(self.numverse)
  }
  return e
def init_pagerecs(filein):
 """ filein is a csv file, with tab-delimiter and with first line as fieldnames
 """
 recs = []
 with codecs.open(filein,"r","utf-8") as f:
  for iline,line in enumerate(f):
   if iline == 0:
    # skip field names
    continue
   pagerec = Pagerec(line,iline)
   if pagerec.parvan != None:
    # skip two blank pages
    recs.append(pagerec)
 print(len(recs),'Page records read from',filein)
 return recs

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
def write(fileout,d):
 with codecs.open(fileout,"w","utf-8") as f:
  jsonstring = json.dumps(d)
  f.write(jsonstring+'\n')
 print('json written to',fileout)
 
if __name__ == "__main__":
 filein=sys.argv[1]  # tab-delimited index file
 fileout = sys.argv[2]
 pagerecs = init_pagerecs(filein)
 parvandict = init_parvandict(pagerecs)
 write(fileout,parvandict)
 
