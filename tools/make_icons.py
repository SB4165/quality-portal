"""Make the Q-badge app icons from the 부적합 변환기 (M-badge) icons.
usage: python make_icons.py <src_dir> <dst_dir>
The M badge (bottom right) is repainted in the same blue and a white bold Q is drawn."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
src=sys.argv[1].rstrip('/')+'/'; dst=sys.argv[2].rstrip('/')+'/'
files={n:n for n in ['icon-192.png','favicon-32.png','icon-512.png','icon-maskable-512.png','apple-touch-icon.png']}
FONT='/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'
for out,f in files.items():
    im=Image.open(src+f).convert('RGBA'); W=im.size[0]; a=np.array(im).astype(int)
    y0=int(W*0.55); sub=a[y0:,y0:]
    blue=(sub[...,2]>110)&(sub[...,0]<60)&(sub[...,3]>200)
    ys,xs=np.nonzero(blue); cx=xs.mean()+y0; cy=ys.mean()+y0
    R=max(xs.max()-xs.min(),ys.max()-ys.min())/2+0.5
    col=tuple(int(v) for v in np.median(sub[blue][:, :3],axis=0))
    wht=(sub[...,0]>200)&(sub[...,1]>200)&(sub[...,2]>200)
    yy,xx=np.mgrid[0:sub.shape[0],0:sub.shape[1]]
    inner=wht&(((xx+y0-cx)**2+(yy+y0-cy)**2)<(R*0.8)**2)
    my=np.nonzero(inner)[0]; capH=(my.max()-my.min()+1) if len(my) else R
    S=8; size=int(np.ceil(R*2+4)); L=Image.new('RGBA',(size*S,size*S),(0,0,0,0)); d=ImageDraw.Draw(L)
    c=size*S/2; d.ellipse([c-R*S,c-R*S,c+R*S,c+R*S],fill=col+(255,))
    # font size so 'Q' cap height (excl. tail) ~= M cap height
    fs=10
    while True:
        ft=ImageFont.truetype(FONT,fs+1); b=ft.getbbox('O',anchor='ls')
        if -b[1]>capH*S: break
        fs+=1
    ft=ImageFont.truetype(FONT,fs); bo=ft.getbbox('O',anchor='ls')
    # center 'O' body vertically on disc center, draw Q at same baseline
    capPx=-bo[1]; base=c+capPx/2
    d.text((c,base),'Q',font=ft,fill=(255,255,255,255),anchor='ms')
    L=L.resize((size,size),Image.LANCZOS)
    ox=int(round(cx-size/2)); oy=int(round(cy-size/2))
    # paste: first clear original badge disc area with blue disc (layer has full disc)
    im.alpha_composite(L,(ox,oy))
    im.save(dst+out, optimize=True)
    print(out,W,round(cx,1),round(cy,1),round(R,1),col,capH)
