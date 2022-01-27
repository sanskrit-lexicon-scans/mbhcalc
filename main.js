// (setq js-indent-level 1)  # for Emacs

function verse_error(verse) {
 let elt=document.getElementById('verse');
 let html = '<p>Could not find verse ' + verse + '</p>';
 elt.innerHTML = html;
}
function get_parvan_name(iparvan) {
 let parvans = ['Ādiparva', 'Sabhāparva', 'Vanaparva', 'Virāṭparva',
  'Udyogaparva', 'Bhīṣmaparva', 'Droṇaparva', 'Karṇaparva', 'Śalyaparva',
  'Sauptikaparva', 'Strīparva', 'Śāntiparva', 'Anuśāsanaparva',
  'Āśvamedhikaparva', 'Āśramavāsikamparva', 'Mausalaparva',
		'Mahāprasthānikaparva', 'Svargārohaṇikaparva'];
 i = iparvan - 1;  // assume iparvan is 1 to 18
 if (i in parvans) {
  return parvans[i];
 }else{
  return 'Unknown Parvan';
 }
}
function verse_id(indexes) {
 [indexprev,indexcur,indexnext] = indexes;
 let vol = indexcur['v'];
 let page = indexcur['page'];
 let v1 = indexcur['v1'];
 let v2 = indexcur['v2'];
 let p = indexcur['p']; // parvan index 1 to 18
 let parvan = get_parvan_name(p);
 let html = `<p>${parvan}, verses ${v1} - ${v2}</p>`;
 let elt = document.getElementById('verseid');
 elt.innerHTML = html;
 elt = document.getElementById('title');
 //html = 
}

function get_verse_from_url() {
 /* two methods to get parvan (P) and verse (Y)
 ?
 ?P.V   P = 1,2,...,18.  V digit string
*/
 let href = window.location.href;
 let url = new URL(href);
 let verse = url.searchParams.get('verse'); // Could be null
 if (verse == null) {
  let search = url.search  // ?X
  verse = search.substr(1)  // drop initial ?
 }
 //console.log('get_verse_from_url: ',verse);
 return verse;
}
function get_index_from_verse(verse,indexdata) {
 // verse = p.v  where p is parvan and v is verse in parvan
 if ((typeof verse) != 'string') {return null;}
 let parts = verse.split('.');
 if (parts.length != 2) {return null;}
 let p = parts[0] // parvan
 let v = parts[1]
 if (! (p in indexdata)) {return null;}
 let parvanpages = indexdata[p];
 let parvanpage = null;
 for (let x of parvanpages) {
  if ((x.v1 <= v) && (v <= x.v2)) {
   parvanpage = x;
   break;
  }
 }
 return parvanpage;
}
function get_indexes_from_verse(verse,indexdata) {
 // verse = p.v  where p is parvan and v is verse in parvan
 // return index info for previous, current, and next page.
 // current page derived from 'verse' (p.v).
 // previous and next page implied.
 ans = [null,null,null];
 if ((typeof verse) != 'string') {return ans;}
 let parts = verse.split('.');
 if (parts.length != 2) {return null;}
 let p = parts[0] // parvan
 let v = parts[1]
 if (! (p in indexdata)) {return ans;}
 let parvanpages = indexdata[p];
 let cur = null;
 let prev = null;
 let next = null;
 let n = parvanpages.length;
 for (let i=0;i<n;i++) {
  let x = parvanpages[i];
  if ((x.v1 <= v) && (v <= x.v2)) {
   cur = x;
   if (i == 0) {
    prev = x;
   }else {
    prev = parvanpages[i-1];
   }
   let j = i+1;
   if (j == n){
    next = x;
   }else {
    next = x[j];
   }
   break;
  }
 }
  return [prev,cur,next];
}

function get_pdfpage_from_index(index) {
/* index is object with keys:
  v: volume, page: page in volume,
  p: parvan (1-18), v1: first verse, v2: last verse
  n: number of verses
 return name of file with the given volume and page
 mbhcalc_v.NNN.pdf  where NNN is 0-filled from page
*/
 if (index == null) {return null;}
 let page = index['page']
 let vol = index['v']
 let text = page.toString();
 let nnn = text.padStart(3,'0');
 let pdf = 'mbhcalc_' + vol + '.' + nnn + '.pdf';
 return pdf
}

function get_verse_html(indexcur) {
 let html = null;
 if (indexcur == null) {return html;}
 let pdfcur = get_pdfpage_from_index(indexcur);
 let urlcur = `pdfpages/${pdfcur}`;
 let android = ` <a href='${urlcur}' style='position:relative; left:100px;'>Click to load pdf</a>`;
 let imageElt = `<object id='servepdf' type='application/pdf' data='${urlcur}' 
              style='width: 98%; height:98%'> ${android} </object>`;
 //console.log('get_verse_html. imageElt=',imageElt);
 return imageElt;
}


function display_verse_html(indexes) {
 verse_id(indexes);
 let html = get_verse_html(indexes[1]);
 let elt=document.getElementById('verse');
 elt.innerHTML = html;
}
function display_verse_url() {
 let pv = get_verse_from_url();
 let indexes = get_indexes_from_verse(pv,indexdata);
 let indexcur = indexes[1];
 if (indexcur == null) {
  verse_error(pv);
  return;
 }
 display_verse_html(indexes);
}
//test();

// indexdata assumed available 
document.getElementsByTagName("BODY")[0].onload = display_verse_url;
/*
file:///E:/sanskrit-lexicon-scans/mbhcalc/pdfpages/mbhcalc_1.418.pdf
file:///E:/pdfwork/mbhcalc/pdfpages/mbhcalc_1.418.pdf

file:///E:/pdfwork/mbhcalc/pdfpages/mbhcalc_1.418.pdf

*/
