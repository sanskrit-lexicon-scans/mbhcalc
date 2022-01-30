import sys,re,codecs
import os

def parse(filename):
 m = re.search(r'^(mbh_calc_)([1-4]) ([0-9]+)[.]pdf$',filename)
 vol = m.group(2)
 page = m.group(3)
 return (vol,page)

def renum_1(vol,page):
 newpage = page
 p = int(page)
 if p == 6:
  return '000a'  # English title page
 if p == 8:
  return '000b'  # Devanagari title page
 if p < 10:
  return None
 if 10 <= p <= 840:
  p1 = p - 9
  newpage = '%s' %p1
  return newpage

def renum_2(vol,page):
 newpage = page
 p = int(page)
 if p == 6:
  return '000a'  # English title page
 if p == 8:
  return '000b'  # Devanagari title page
 if p < 10:
  return None
 if 10 <= p <= 133:
  p1 = p - 9
 elif p <= 873:
  p1 = p - 5
 else:
  return None
 newpage = '%s' %p1
 return newpage

def renum_3(vol,page):
 newpage = page
 p = int(page)
 if p == 6:
  return '000a'  # English title page
 if p == 8:
  return '000b'  # Devanagari title page
 if p < 10:
  return None
 if 10 <= p <= 506:
  p1 = p - 9
 elif p <= 866:
  p1 = p - 5
 else:
  return None
 newpage = '%s' %p1
 return newpage

def renum_4(vol,page):
 newpage = page
 p = int(page)
 if p == 6:
  return '000a'  # English title page
 if p == 8:
  return '000b'  # Devanagari title page
 if p < 10:
  return None
 if 10 <= p <= 452:
  p1 = p - 9
  newpage = '%s' %p1
  return newpage
 else:
  return None
 
def makesh(vol,filenames):
 ans = []
 renumF = globals()['renum_%s' % vol]
 pages = []
 for ifile,filename in enumerate(filenames):
  v,p = parse(filename)
  assert v == vol
  pages.append((p,filename))
 pages = sorted(pages,key = lambda x: int(x[0]))
 for p,filename in pages:
  newp = renumF(vol,p)
  if newp == None:
   continue  # skip this page
  oldpath = 'vol%s/%s' %(vol,filename)
  if newp in ['000a','000b']:
   newp1 = newp #title
  else:
   newp1 = '%03d' %int(newp)
  newpath = 'pdfpages/mbhcalc_%s.%s.pdf' %(vol,newp1)
  sh = "cp '%s' %s" %(oldpath,newpath)  # oldpath has a space, hence '%s'
  ans.append(sh)
 return ans 

def write_script(fileout,shfiles):
 with codecs.open(fileout,"w","utf-8") as f:
  for vol,shfile in shfiles:
   n = len(shfile)
   print('generating vol %s' %vol,'%s copies' % n)
   f.write('echo "copying %s files from vol%s"\n' %(n,vol))
   for sh in shfile:
    f.write(sh+'\n')
if __name__ == "__main__":
 fileout = sys.argv[1]
 #volfiles = []
 shfiles = []
 for vol in ['1','2','3','4']:
  filenames = os.listdir('vol%s'% vol)
  #volfiles.append(filenames)
  print(vol,len(filenames))
  shfile = makesh(vol,filenames)

  shfiles.append((vol,shfile))
 write_script(fileout,shfiles)
 
