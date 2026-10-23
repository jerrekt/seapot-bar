# Seapot bar guide QR chip, 2.5in x 2.5in (63.5mm). Two-part: black base + white face (modules cut through).
# Print: pause at Z=BASE (2.4mm) and swap black -> white, same as the menu chip.
import qrcode, trimesh
from shapely.geometry import box
from shapely.ops import unary_union
from shapely import affinity
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties
from shapely.geometry import Polygon
URL="https://seapot-bar.adsuaracloud.com"
SIZE=63.5; R=5.0; BASE=2.4; FACE_H=0.6; FACE=SIZE-4; FR=3.5; QR_MM=44.0; QR_TOP=SIZE/2-7.5
def rrect(w,h,r): return box(-w/2+r,-h/2+r,w/2-r,h/2-r).buffer(r,resolution=24)
def text_poly(s,height,font,cx,cy,max_w=None):
    fp=FontProperties(fname=font); tp=TextPath((0,0),s,size=10,prop=fp)
    g=Polygon()
    for p in sorted([Polygon(p) for p in tp.to_polygons() if len(p)>2],key=lambda p:-p.area): g=g.symmetric_difference(p.buffer(0))
    H=TextPath((0,0),"H",size=10,prop=fp).get_extents().height; k=height/H
    g=affinity.scale(g,k,k,origin=(0,0))
    if max_w and g.bounds[2]-g.bounds[0]>max_w: g=affinity.scale(g,max_w/(g.bounds[2]-g.bounds[0]),1,origin=(0,0))
    b=g.bounds; return affinity.translate(g,cx-(b[0]+b[2])/2,cy-(b[1]+b[3])/2)
def extrude(poly,h,z0=0):
    ps=list(poly.geoms) if hasattr(poly,'geoms') else [poly]
    m=trimesh.util.concatenate([trimesh.creation.extrude_polygon(p,h) for p in ps if p.area>1e-4]); m.apply_translation([0,0,z0]); return m
q=qrcode.QRCode(border=0,error_correction=qrcode.constants.ERROR_CORRECT_M); q.add_data(URL); q.make()
M=q.get_matrix(); N=len(M); m=QR_MM/N; left=-QR_MM/2
modules=unary_union([box(left+x*m,QR_TOP-(y+1)*m,left+(x+1)*m,QR_TOP-y*m) for y,r in enumerate(M) for x,v in enumerate(r) if v])
label=text_poly("STAFF BAR GUIDE",3.4,"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",0,QR_TOP-QR_MM-4.2,max_w=44)
face=rrect(FACE,FACE,FR).difference(modules.buffer(0.03,join_style=2)).difference(label)
base=extrude(rrect(SIZE,SIZE,R),BASE); facem=extrude(face,FACE_H,BASE)
base.export("seapot-bar-qr-base-black.stl"); facem.export("seapot-bar-qr-face-white.stl")
trimesh.util.concatenate([base,facem]).export("seapot-bar-qr.stl")
print(N,"modules",round(m,2),"mm each", base.bounds.tolist())
