import json,os,random,sys,urllib.request
V=[0,100,320,330,500,900,0]
B=[0]*128
S=0; C=0; E=-1; K=[0,0]
KEEP=[15]*128
KEEP[0]=7; KEEP[7]=11; KEEP[112]=13; KEEP[119]=14; KEEP[4]=3; KEEP[116]=12
NP=(-33,-31,-18,-14,14,18,31,33)
KP=(-17,-16,-15,-1,1,15,16,17)
DP=(-17,-15,15,17); RP=(-16,-1,1,16)
SQ=[s for s in range(128) if not s&136]
MIR=[((7-(s>>4))<<4)+(s&7) for s in range(128)]
PA=[0,0,4,8,14,24,40,0]; PC=[0,0,0,10,15,10,5,0]
KF=[20,25,10,0,0,10,25,20]
PST=[[0]*128 for _ in range(7)]
for s in SQ:
    r=s>>4; f=s&7; rw=7-r
    cen=min(f,7-f)+min(r,7-r)
    PST[1][s]=PA[rw]+(PC[rw] if f in (3,4) else 0)
    PST[2][s]=6*cen-20
    PST[3][s]=4*cen-8
    PST[4][s]=15 if rw==6 else 0
    PST[5][s]=2*cen-6
ZR=random.Random(20261113)
ZB=[[ZR.getrandbits(64) for _ in range(15)] for _ in range(128)]
ZS=ZR.getrandbits(64)
ZC=[ZR.getrandbits(64) for _ in range(16)]
ZE=[ZR.getrandbits(64) for _ in range(8)]
H=[0]

def atk(s,by):
    for d in ((15,17) if by==0 else (-15,-17)):
        t=s+d
        if not t&136 and B[t]==(1|by<<3): return 1
    for d in NP:
        t=s+d
        if not t&136 and B[t]==(2|by<<3): return 1
    for d in KP:
        t=s+d
        if not t&136 and B[t]==(6|by<<3): return 1
    for ds,ts in ((DP,(3,5)),(RP,(4,5))):
        for d in ds:
            t=s+d
            while not t&136:
                p=B[t]
                if p:
                    if (p>>3)==by and (p&7) in ts: return 1
                    break
                t += d
    return 0

def gen(cap=0):
    ms=[]
    for s in SQ:
        p=B[s]
        if not p or (p>>3)!=S: continue
        t=p&7
        if t==1:
            d=-16 if S==0 else 16
            prom=0 if S==0 else 7
            o=s+d
            if not B[o] and (not cap or (o>>4)==prom):
                if (o>>4)==prom:
                    for pr in (5,4,3,2): ms.append(s|o<<7|pr<<14)
                elif not cap:
                    ms.append(s|o<<7)
                    if (s>>4)==(6 if S==0 else 1) and not B[o+d]:
                        ms.append(s|(o+d)<<7)
            for d2 in (d-1,d+1):
                o=s+d2
                if o&136: continue
                q=B[o]
                if q and (q>>3)!=S:
                    if (o>>4)==prom:
                        for pr in (5,4,3,2): ms.append(s|o<<7|pr<<14)
                    else: ms.append(s|o<<7)
                elif o==E: ms.append(s|o<<7)
        elif t in (2,6):
            for d in (NP if t==2 else KP):
                o=s+d
                if o&136: continue
                q=B[o]
                if not q or (q>>3)!=S:
                    if not cap or q: ms.append(s|o<<7)
            if t==6 and not cap:
                home=116 if S==0 else 4
                if s==home:
                    specs=((1,(117,118),(116,117,118),118),(2,(113,114,115),(114,115,116),114)) if S==0 else \
                            ((4,(5,6),(4,5,6),6),(8,(1,2,3),(2,3,4),2))
                    for bit,empt,path,dest in specs:
                        if C&bit and all(not B[x] for x in empt) and all(not atk(x,S^1) for x in path):
                            ms.append(s|dest<<7)
        else:
            for d in (DP if t==3 else RP if t==4 else KP):
                o=s+d
                while not o&136:
                    q=B[o]
                    if not q:
                        if not cap: ms.append(s|o<<7)
                    else:
                        if (q>>3)!=S: ms.append(s|o<<7)
                        break
                    o += d
    return ms

def make(m):
    global S,C,E
    s=m&127; o=(m>>7)&127; pr=(m>>14)&7; p=B[s]
    cap=B[o]; ep=E; oc=C; cs=-1; oh=H[0]
    h=oh^ZS^ZC[oc]
    if ep>=0: h ^= ZE[ep&7]
    if (p&7)==1 and o==E and not cap and (s&7)!=(o&7):
        cs=o+16 if S==0 else o-16
        cap=B[cs]; B[cs]=0
        h ^= ZB[cs][cap]
    elif cap: h ^= ZB[o][cap]
    np_=(pr|S<<3) if pr else p
    h ^= ZB[s][p]^ZB[o][np_]
    B[o]=np_
    B[s]=0
    if (p&7)==6:
        K[S]=o
        if o-s==2:
            rp=B[s+3]; B[s+1]=rp; B[s+3]=0
            h ^= ZB[s+3][rp]^ZB[s+1][rp]
        elif s-o==2:
            rp=B[s-4]; B[s-1]=rp; B[s-4]=0
            h ^= ZB[s-4][rp]^ZB[s-1][rp]
    C &= KEEP[s]&KEEP[o]
    E=o+(16 if S==0 else -16) if (p&7)==1 and abs(o-s)==32 else -1
    h ^= ZC[C]
    if E>=0: h ^= ZE[E&7]
    H[0]=h
    S ^= 1
    return (cap,cs,ep,oc,oh)

def unmake(m,u):
    global S,C,E
    cap,cs,ep,oc,oh=u
    H[0]=oh
    S ^= 1
    s=m&127; o=(m>>7)&127; pr=(m>>14)&7
    p=B[o]
    B[s]=(1|S<<3) if pr else p
    B[o]=0
    if (B[s]&7)==6:
        K[S]=s
        if o-s==2: B[s+3]=B[s+1]; B[s+1]=0
        elif s-o==2: B[s-4]=B[s-1]; B[s-1]=0
    if cs>=0: B[cs]=cap
    elif cap: B[o]=cap
    C=oc; E=ep

def ev():
    tot=0; bp=[0,0]; mat=0; kp=[0,0]
    PM=[[0]*8,[0]*8]; RF=[0,0]
    for s in SQ:
        p=B[s]
        if not p: continue
        t=p&7; c=p>>3
        if t==6: kp[c]=s; continue
        v=V[t]+PST[t][s if c==0 else MIR[s]]
        if t==1: PM[c][s&7] |= 1<<(s>>4)
        if t==3: bp[c] += 1
        if t==4: RF[c] |= 1<<(s&7)
        if t>1: mat += V[t]
        tot += v if c==0 else -v
    PB=[0,0,5,10,20,35,60,0]
    for c in (0,1):
        for f in range(8):
            mask=PM[c][f]
            cnt=bin(mask).count("1")
            if cnt>1: tot += (-12*(cnt-1)) if c==0 else (12*(cnt-1))
            if RF[c]>>f&1:
                if not (PM[0][f]|PM[1][f]): tot += 15 if c==0 else -15
                elif not PM[c][f]: tot += 8 if c==0 else -8
            em=PM[1-c][f]
            if f>0: em |= PM[1-c][f-1]
            if f<7: em |= PM[1-c][f+1]
            mm=mask
            while mm:
                r=(mm&-mm).bit_length()-1
                mm &= mm-1
                ahead=((1<<r)-1) if c==0 else (0xFF^((1<<(r+1))-1))
                if not em&ahead:
                    rw=(7-r) if c==0 else r
                    tot += PB[rw] if c==0 else -PB[rw]
    for c in (0,1):
        s=kp[c]; r=s>>4; f=s&7
        rw=(7-r) if c==0 else r
        cen=min(f,7-f)+min(r,7-r)
        v=(8*cen-24) if mat<=1300 else (KF[f] if rw==0 else max(-50,-15*rw))
        if mat>1300 and rw<=1:
            step=-16 if c==0 else 16
            for df in (-1,0,1):
                t2=s+step+df
                if not t2&136 and B[t2]==(1|c<<3): v += 10
        tot += v if c==0 else -v
    if bp[0]>1: tot += 45
    if bp[1]>1: tot -= 45
    return tot if S==0 else -tot

ND=[0]; LIM=[40000]; AB=[0]; TT={}; KL={}; HI={}
PH=[0]*512; GH=[]
def sc(m):
    o=(m>>7)&127; q=B[o]
    v=V[q&7] if q else (100 if (B[m&127]&7)==1 and o==E else 0)
    r=10*v-(B[m&127]&7) if v else 0
    if q and v<V[B[m&127]&7] and atk(o,S^1): r-=2*(V[B[m&127]&7]-v)
    pr=(m>>14)&7
    return r+2000+V[pr] if pr else r

def legal(cap=0):
    out=[]
    for m in gen(cap):
        u=make(m)
        if not atk(K[S^1],S): out.append(m)
        unmake(m,u)
    return out

def qs(a,b,ply):
    ND[0] += 1
    if ND[0]>LIM[0]: AB[0]=1; return 0
    chk=atk(K[S],S^1)
    best=-100001
    if not chk:
        st=ev()
        if st>=b: return st
        best=st
        if st>a: a=st
    ms=legal(0 if chk else 1)
    ms.sort(key=sc,reverse=True)
    for m in ms:
        if not chk and not (m>>14)&7 and st+(V[B[(m>>7)&127]&7] if B[(m>>7)&127] else 100)+200<=a: continue
        u=make(m); s2=-qs(-b,-a,ply+1); unmake(m,u)
        if AB[0]: return 0
        if s2>best: best=s2
        if s2>=b: return s2
        if s2>a: a=s2
    if chk and not ms: return -100000+ply
    return best

def neg(d,a,b,ply):
    global S,E
    if ply<512: PH[ply]=H[0]
    if d<=0: return qs(a,b,ply)
    ND[0] += 1
    if ND[0]>LIM[0]: AB[0]=1; return 0
    chk=atk(K[S],S^1)
    if chk: d += 1
    key=H[0]
    ent=TT.get(key); tm=0
    if ent:
        ed,es,ef,tm=ent
        if ed>=d:
            if ef==0: return es
            if ef==1 and es>=b: return es
            if ef==2 and es<=a: return es
    if d>=4 and not chk and ply>0:
        npm=0
        for s in SQ:
            p=B[s]
            if p and (p>>3)==S and (p&7) in (2,3,4,5): npm += V[p&7]
        if npm>=500 and ev()>=b:
            oe=E; oh=H[0]
            E=-1; S ^= 1; H[0]=oh^ZS^(ZE[oe&7] if oe>=0 else 0)
            s2=-neg(d-3,-b,-b+1,ply+1)
            S ^= 1; E=oe; H[0]=oh
            if AB[0]: return 0
            if s2>=b: return b
    a0=a
    ms=legal()
    if not ms: return -100000+ply if chk else 0
    se=ev() if d<=2 and not chk else 0
    kl=KL.get(ply,())
    ms.sort(key=lambda m: (m==tm,sc(m)+(4000 if m in kl else 0)+min(HI.get(m,0),1500)),reverse=True)
    best=-100001; bm=0
    for i,m in enumerate(ms):
        quiet=not sc(m)
        if d<=2 and i>=3 and quiet and m not in kl and se+(250 if d==1 else 500)<=a: continue
        u=make(m)
        if ply>=2 and (H[0]==PH[ply-2] or (ply>=4 and H[0]==PH[ply-4])):
            s2=0
        elif d>=3 and i>=3 and quiet and m not in kl:
            s2=-neg(d-2,-a-1,-a,ply+1)
            if AB[0]: unmake(m,u); return 0
            if s2>a: s2=-neg(d-1,-b,-a,ply+1)
        elif i:
            s2=-neg(d-1,-a-1,-a,ply+1)
            if AB[0]: unmake(m,u); return 0
            if s2>a: s2=-neg(d-1,-b,-a,ply+1)
        else:
            s2=-neg(d-1,-b,-a,ply+1)
        unmake(m,u)
        if AB[0]: return 0
        if s2>best: best=s2; bm=m
        if s2>a: a=s2
        if a>=b:
            if quiet:
                KL[ply]=(m,)+kl[:1]
                HI[m]=HI.get(m,0)+d*d
            break
    TT[key]=(d,best,0 if a0<best<b else 1 if best>=b else 2,bm)
    return best

def uci(m):
    sq=lambda x: "abcdefgh"[x&7]+str(8-(x>>4))
    pr=(m>>14)&7
    return sq(m&127)+sq((m>>7)&127)+(("  nbrq"[pr]) if pr else "")

def parse(fen):
    global S,C,E
    ps=fen.split()
    for i in range(128): B[i]=0
    for ri,row in enumerate(ps[0].split("/")):
        f=0
        for ch in row:
            if ch.isdigit(): f += int(ch)
            else:
                s=ri*16+f
                t="pnbrqk".index(ch.lower())+1
                B[s]=t|(8 if ch.islower() else 0)
                if t==6: K[1 if ch.islower() else 0]=s
                f += 1
    S=0 if ps[1]=="w" else 1
    C=0
    for ch,bit in (("K",1),("Q",2),("k",4),("q",8)):
        if ch in ps[2]: C |= bit
    E=-1
    if ps[3]!="-": E=(8-int(ps[3][1]))*16+"abcdefgh".index(ps[3][0])
    h=ZC[C]
    if S: h ^= ZS
    if E>=0: h ^= ZE[E&7]
    for s in SQ:
        if B[s]: h ^= ZB[s][B[s]]
    H[0]=h

def choose(fen,legal_list):
    parse(fen); PH[0]=H[0]
    if len(TT)>300000: TT.clear()
    ND[0]=0; AB[0]=0
    by={uci(m): m for m in legal()}
    cand=[by[u] for u in legal_list if u in by] or list(by.values())
    cand.sort(key=sc,reverse=True)
    best=cand[0]
    for d in range(1,64):
        AB[0]=0; a=-100001; scored=[]
        for m in cand:
            u=make(m); s2=0 if GH.count(H[0])>=2 else -neg(d-1,-100001,-a,1); unmake(m,u)
            if AB[0]: break
            scored.append((s2,m))
            if s2>a: a=s2
        if AB[0]: break
        scored.sort(key=lambda x: -x[0])
        cand=[m for _,m in scored]
        best=cand[0]
        if a>99000: break
    return uci(best)

U=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
def post(pth,body):
    rq=urllib.request.Request(U+pth,data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(rq) as rs: return json.load(rs)

def setgh(g):
    global GH
    parse(g["start_fen"]); GH=[H[0]]
    for u in g["moves"]:
        make(next(m for m in gen() if uci(m)==u)); GH.append(H[0])

while True:
    g=post("/game",{})
    if g["status"]=="done": break
    while g["status"]=="your_move":
        setgh(g)
        g=post("/move",{"game": g["game"],"move": choose(g["fen"],g["legal_moves"])})
