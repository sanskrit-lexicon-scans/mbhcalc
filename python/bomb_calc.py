# coding=utf-8
"""
 python temp.py temp_bomb.txt temp_calc.txt temp_bomb_calc.txt

"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(outarr),"lines written to",fileout)

def make_outarr_helper(line):
 key,val = line.split(':')
 key = key.rstrip()
 val = val.strip()
 if key == 'Total verses':
  key = 'Tot'
 return key,val
def make_outarr(linesb,linesc):
 outarr = []
 out = '\t'.join(['parvan','bombay','calcutta'])
 outarr.append(out)
 for i,lineb in enumerate(linesb):
  linec = linesc[i]
  kb,valb = make_outarr_helper(lineb)
  kc,valc = make_outarr_helper(linec)
  assert kb == kc
  ivalb = int(valb)
  ivalc = int(valc)
  out = '%s\t%5d\t%5d' % (kb,ivalb,ivalc)
  outarr.append(out)
 return outarr
  
  
if __name__ == "__main__":
 filein1=sys.argv[1]  # bomb
 filein2=sys.argv[2]  # calc
 fileout = sys.argv[3] # bomb_calc

 linesb = read_lines(filein1)
 linesc = read_lines(filein2)
 assert len(linesb) == len(linesc)
 outarr = make_outarr(linesb,linesc)
 write_lines(fileout,outarr)

 
