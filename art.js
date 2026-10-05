// ---------- Illustrationen ----------
function rng(seed){ let x = seed*9301 + 49297; return () => (x = (x*9301 + 49297) % 233280) / 233280; }
const SKIES = [['#7fb3e6','#cfe3f5','#f6e7cf'],['#5d93d1','#a9cdee','#f3d9b5'],['#8db7e0','#dcebf7','#fbe9d0'],['#4f86c6','#9fc6ea','#f1d3a8'],['#76a9dd','#c7def3','#f7e3c6'],['#6c9fd6','#bcd7f1','#f5ddb9']];
function ridge(r, w, base, amp, n, rough){
  const pts = []; for (let i = 0; i <= n; i++){ const x = i/n*w; pts.push([x, base - amp*(0.45 + 0.55*Math.sin(i*1.7 + r()*2))*(0.6 + r()*rough)]); }
  return 'M0,' + base + ' ' + pts.map(p => 'L' + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ') + ' L' + w + ',' + base + ' L' + w + ',1000 L0,1000 Z';
}
function trees(r, w, y0, y1, n, palette, scale){
  let o = ''; for (let i = 0; i < n; i++){ const x = r()*w, y = y0 + r()*(y1 - y0), h = (14 + r()*16)*scale*(0.6 + (y - y0)/(y1 - y0 + 1)*0.8), c = palette[Math.floor(r()*palette.length)];
    o += '<path d="M'+x.toFixed(1)+','+(y-h).toFixed(1)+' L'+(x-h*0.32).toFixed(1)+','+y.toFixed(1)+' L'+(x+h*0.32).toFixed(1)+','+y.toFixed(1)+' Z" fill="'+c+'"/>'; }
  return o;
}
const AUTUMN = ['#2f5a3a','#3b6b45','#c9762d','#d9902f','#9c4a22','#284d33','#e2a43b'];
function tourArt(t, W, H){
  W = W || 640; H = H || 360;
  const r = rng(t.nr*7 + 3), sky = SKIES[(t.nr - 1) % SKIES.length], id = 'g' + t.nr + '_' + W;
  const hi = Math.min(1, Math.max(0.12, (t.top - 600)/1600));
  let peakX = W*(0.48 + r()*0.16), peakY = H*(0.70 - hi*0.52), baseY = H*0.80;
  const lw = W*(0.42 + r()*0.08), rw = W*(0.40 + r()*0.08);
  const valley = t.top < 1000;
  const j = () => (r() - 0.5);
  let mPts, mPath, snow = '', route, sx, sy, fx, fy;
  if (!valley){
    mPts = [[peakX - lw, baseY],[peakX - lw*(0.62 + j()*0.2), baseY - (baseY - peakY)*(0.35 + j()*0.2)],[peakX - lw*(0.33 + j()*0.15), baseY - (baseY - peakY)*(0.66 + j()*0.15)],[peakX - lw*0.12, peakY + (baseY - peakY)*(0.08 + r()*0.08)],[peakX, peakY],[peakX + rw*(0.12 + r()*0.08), peakY + (baseY - peakY)*(0.12 + r()*0.1)],[peakX + rw*(0.36 + j()*0.15), baseY - (baseY - peakY)*(0.6 + j()*0.2)],[peakX + rw*(0.68 + j()*0.15), baseY - (baseY - peakY)*(0.3 + j()*0.15)],[peakX + rw, baseY]];
    if (r() > 0.4){ const k = 0.32 + r()*0.2; mPts.splice(7, 0, [peakX + rw*(0.5 + j()*0.1), baseY - (baseY - peakY)*k]); }
    mPath = 'M' + mPts.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' L') + ' Z';
    if (t.top > 1700) snow = '<path d="M'+(peakX - lw*0.13).toFixed(1)+','+(peakY + (baseY-peakY)*0.12).toFixed(1)+' L'+peakX.toFixed(1)+','+peakY.toFixed(1)+' L'+(peakX + rw*0.15).toFixed(1)+','+(peakY + (baseY-peakY)*0.17).toFixed(1)+' L'+(peakX+rw*0.05).toFixed(1)+','+(peakY+(baseY-peakY)*0.13).toFixed(1)+' L'+(peakX-lw*0.03).toFixed(1)+','+(peakY+(baseY-peakY)*0.19).toFixed(1)+' Z" fill="#fff" opacity=".92"/>';
    sx = peakX - lw*0.78; sy = baseY - 6; fx = peakX; fy = peakY;
    route = 'M'+sx.toFixed(1)+','+sy.toFixed(1)+' C'+(sx + (peakX - sx)*0.35).toFixed(1)+','+(sy - 4).toFixed(1)+' '+(peakX - lw*0.45).toFixed(1)+','+(peakY + (baseY-peakY)*0.55).toFixed(1)+' '+(peakX - lw*0.25).toFixed(1)+','+(peakY + (baseY-peakY)*0.42).toFixed(1)+' S'+(peakX - lw*0.05).toFixed(1)+','+(peakY + (baseY-peakY)*0.08).toFixed(1)+' '+peakX.toFixed(1)+','+(peakY + 2).toFixed(1);
  } else {
    // Talrunde: hohe Kulisse hinten, Weg durch Wiesen vorne
    const peaks = [[W*(0.2 + j()*0.1), H*0.22],[W*(0.55 + j()*0.1), H*0.14],[W*(0.85 + j()*0.08), H*0.26]];
    mPath = peaks.map(([x, y]) => { const w = W*0.26; return 'M'+(x-w).toFixed(1)+','+(H*0.66).toFixed(1)+' L'+(x-w*0.35).toFixed(1)+','+(y+H*0.14).toFixed(1)+' L'+x.toFixed(1)+','+y.toFixed(1)+' L'+(x+w*0.3).toFixed(1)+','+(y+H*0.12).toFixed(1)+' L'+(x+w).toFixed(1)+','+(H*0.66).toFixed(1)+' Z'; }).join(' ');
    snow = peaks.map(([x, y]) => { const w = W*0.26; return '<path d="M'+(x-w*0.1).toFixed(1)+','+(y+H*0.04).toFixed(1)+' L'+x.toFixed(1)+','+y.toFixed(1)+' L'+(x+w*0.1).toFixed(1)+','+(y+H*0.04).toFixed(1)+' L'+(x+w*0.02).toFixed(1)+','+(y+H*0.06).toFixed(1)+' Z" fill="#fff" opacity=".9"/>'; }).join('');
    sx = W*0.08; sy = H*0.90; fx = W*0.86; fy = H*0.80;
    route = 'M'+sx.toFixed(1)+','+sy.toFixed(1)+' C'+(W*0.3).toFixed(1)+','+(H*0.80).toFixed(1)+' '+(W*0.42).toFixed(1)+','+(H*0.95).toFixed(1)+' '+(W*0.6).toFixed(1)+','+(H*0.86).toFixed(1)+' S'+(W*0.78).toFixed(1)+','+(H*0.78).toFixed(1)+' '+fx.toFixed(1)+','+fy.toFixed(1);
    baseY = H*0.70;
  }
  const sun = '<circle cx="'+(W*(0.15 + r()*0.2)).toFixed(1)+'" cy="'+(H*(0.18 + r()*0.08)).toFixed(1)+'" r="'+(H*0.07).toFixed(1)+'" fill="#fff6dc" opacity=".9"/>';
  const clouds = [0,1].map(i => { const cx = r()*W, cy = H*(0.12 + r()*0.18), s = 0.6 + r()*0.7; return '<g opacity=".75" fill="#fff"><ellipse cx="'+cx.toFixed(1)+'" cy="'+cy.toFixed(1)+'" rx="'+(46*s).toFixed(1)+'" ry="'+(11*s).toFixed(1)+'"/><ellipse cx="'+(cx+18*s).toFixed(1)+'" cy="'+(cy-8*s).toFixed(1)+'" rx="'+(26*s).toFixed(1)+'" ry="'+(12*s).toFixed(1)+'"/></g>'; }).join('');
  const water = valley ? '<path d="M0,'+(H*0.93).toFixed(1)+' C'+(W*0.3).toFixed(1)+','+(H*0.88).toFixed(1)+' '+(W*0.6).toFixed(1)+','+(H*0.98).toFixed(1)+' '+W+','+(H*0.91).toFixed(1)+' L'+W+','+(H*0.96).toFixed(1)+' C'+(W*0.6).toFixed(1)+','+(H*1.02).toFixed(1)+' '+(W*0.3).toFixed(1)+','+(H*0.93).toFixed(1)+' 0,'+(H*0.98).toFixed(1)+' Z" fill="#7fb0d8" opacity=".85"/>' : '';
  const flag = '<g transform="translate('+fx.toFixed(1)+','+fy.toFixed(1)+')"><line x1="0" y1="0" x2="0" y2="-22" stroke="#1b2a40" stroke-width="2"/><path d="M0,-22 L15,-17 L0,-12 Z" fill="#eb6834"/></g>';
  return '<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Illustration '+t.kurz+'">'+
    '<defs><linearGradient id="s'+id+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+sky[0]+'"/><stop offset=".6" stop-color="'+sky[1]+'"/><stop offset="1" stop-color="'+sky[2]+'"/></linearGradient>'+
    '<linearGradient id="m'+id+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8f9bab"/><stop offset=".55" stop-color="#6c7a8c"/><stop offset="1" stop-color="#4c596b"/></linearGradient>'+
    '<linearGradient id="v'+id+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f9a52"/><stop offset="1" stop-color="#55703a"/></linearGradient></defs>'+
    '<rect width="'+W+'" height="'+H+'" fill="url(#s'+id+')"/>'+sun+clouds+
    '<path d="'+ridge(r, W, H*0.66, H*0.22, 9, 0.6)+'" fill="#a9b9cf" opacity=".75"/>'+
    '<path d="'+ridge(r, W, H*0.72, H*0.14, 12, 0.5)+'" fill="#8ea2bb" opacity=".8"/>'+
    '<path d="'+mPath+'" fill="url(#m'+id+')"/>'+snow+
    '<path d="'+mPath+'" fill="none"/>'+
    '<path d="'+ridge(r, W, valley ? H*0.74 : H*0.86, H*0.08, 14, 0.4)+'" fill="url(#v'+id+')"/>'+
    (valley ? trees(r, W, H*0.70, H*0.78, Math.round(W/12), AUTUMN, H/360*0.8) + '<rect x="0" y="'+(H*0.78).toFixed(1)+'" width="'+W+'" height="'+(H*0.22).toFixed(1)+'" fill="#8aa55a"/>' + water : trees(r, W, H*0.80, H*0.97, Math.round(W/9), AUTUMN, H/360))+
    '<path d="'+route+'" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".55"/>'+
    '<path d="'+route+'" fill="none" stroke="#eb6834" stroke-width="2.6" stroke-dasharray="7 6" stroke-linecap="round"/>'+
    '<circle cx="'+sx.toFixed(1)+'" cy="'+sy.toFixed(1)+'" r="5" fill="#fff" stroke="#eb6834" stroke-width="2.5"/>'+flag+'</svg>';
}
function heroArt(){
  const W = 1600, H = 600, r = rng(42);
  const far = ridge(r, W, H*0.58, H*0.26, 16, 0.7), mid = ridge(r, W, H*0.68, H*0.22, 20, 0.6), near = ridge(r, W, H*0.80, H*0.14, 24, 0.5);
  let peaks = ''; [[0.18,0.30],[0.47,0.22],[0.74,0.27]].forEach(([px, py]) => { const x = W*px, y = H*py, w = W*0.17;
    peaks += '<path d="M'+(x-w)+','+(H*0.62)+' L'+(x-w*0.4)+','+(y+H*0.15)+' L'+(x-w*0.1)+','+(y+H*0.03)+' L'+x+','+y+' L'+(x+w*0.2)+','+(y+H*0.06)+' L'+(x+w*0.5)+','+(y+H*0.18)+' L'+(x+w)+','+(H*0.62)+' Z" fill="url(#hm)"/>'+
             '<path d="M'+(x-w*0.12)+','+(y+H*0.04)+' L'+x+','+y+' L'+(x+w*0.22)+','+(y+H*0.07)+' L'+(x+w*0.08)+','+(y+H*0.06)+' L'+(x-w*0.02)+','+(y+H*0.09)+' Z" fill="#fff" opacity=".9"/>'; });
  const chalet = '<g transform="translate('+(W*0.62)+','+(H*0.80)+')"><rect x="-34" y="-30" width="68" height="34" fill="#7a4a2a"/><path d="M-44,-28 L0,-62 L44,-28 Z" fill="#4a2c1a"/><rect x="-10" y="-14" width="14" height="18" fill="#f4c46a"/><rect x="12" y="-22" width="12" height="10" fill="#f4c46a"/><rect x="18" y="-58" width="7" height="16" fill="#4a2c1a"/></g>';
  $('hero-art').innerHTML = '<defs><linearGradient id="hs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f6fae"/><stop offset=".55" stop-color="#9cc0e4"/><stop offset="1" stop-color="#f3cf9c"/></linearGradient>'+
    '<linearGradient id="hm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9aa6b6"/><stop offset="1" stop-color="#55627a"/></linearGradient>'+
    '<radialGradient id="hsun"><stop offset="0" stop-color="#fff4d6"/><stop offset="1" stop-color="#fff4d6" stop-opacity="0"/></radialGradient></defs>'+
    '<rect width="'+W+'" height="'+H+'" fill="url(#hs)"/><circle cx="'+(W*0.86)+'" cy="'+(H*0.30)+'" r="160" fill="url(#hsun)"/><circle cx="'+(W*0.86)+'" cy="'+(H*0.30)+'" r="34" fill="#fff6df"/>'+
    '<path d="'+far+'" fill="#b4c2d6" opacity=".7"/>'+peaks+'<path d="'+mid+'" fill="#6f8aa6" opacity=".85"/>'+
    '<path d="'+near+'" fill="#58703f"/>'+trees(r, W, H*0.76, H*1.0, 150, AUTUMN, 1.6)+chalet;
}
