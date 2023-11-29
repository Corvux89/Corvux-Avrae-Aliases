!alias tool <drac2>
ch=character()
lj,gv,M,cv,g=load_json,get_gvar,(s:=str).replace,ch.set_cvar,get
B,D,V="!",{"O":"&1&","T":"&2&"},3.5
G,I,N=lj(gv("2408a8c0-eb9a-4df7-b9d3-ae94ca6493c4")),gv(D.T)," ".join(&ARGS&[2:])
if I:
 cv(G.s,D.T)
W,U,A=not"&"in"&2&",V<G.m[13],G.a[:8]
u,b=lj(g(G.E,"[]")),lj(gv(g(G.s,""))or"[]")
P,E,l=g(G.p,""),g(G.e,""),G.H+b+u
Z,c=len(G.c),G.c+[x.t for x in l]
D['p'],D['e']=P,E
z=[[D.update({x:M(D[x].lower(),y,"")})for y in G[B]]for x in D]
m=min(([c.index(x)for x in c if D.O in x]+[0])[0],Z)
t=(([x for x in l if(D.O if m==Z else D.T)in x.t]if m!=6 else[{"t":D.T,"n":"&2&","d":N}])or[G.m[12]])[0]
D['P'],D['E']=P,E
P,E,e,p=[D[x].split(","+(" "*(x in "PE"))) if D[x] else [] for x in G.Y]
j=int(g(G.l,0))>1
r,o=g(G.r),3 if e and[x for x in e if D.O in x]else 2 if p and[x for x in p if D.O in x]else 1 if j else 0
Q=P if m<3 else E if m<5 else lj(g(G.E,"[]"))
q=t in Q
Q.append(t.n if m<6 else t)if(not t.n in Q)*(m in[1,3])or(m==6)*(not q)else Q.remove(t.n if m<7 else t)if(m in[2,4]and t.n in Q)or(m==7 and q)else""
J=floor(r*ch.skills.strength.prof)
r=f'-b "{floor(r*(G.é[o].m))-J}{G.é[o].t}"'+(G.J if J else"")
cv(("p"if m<3 else"e"if m<5 else"extra")+"Tools",", ".join(Q) if m<5 else dump_json(Q))if(0<m<5 or 5<m<8)*(W)else""
C=[M(M(name,"'",r"\'"),'"',r'\"'),t.n if t.n else D.T,t.d,t.t,g(G.E,"[]"),D.T,r,str(V)+G.P*U,M(gv(G.L),G.A,G.S*(D.T in'server')or G.A),M(g(G.p)or G.N,", ","\n"),M(g(G.e)or G.N,", ","\n"),color,image,f"a{'n'*(D.T[0]in'iI')} ["]
F=(m in[1,3])*(t.t)or(m==2)*(t.n in D.P)or(m==4)*(t.n in D.E)or(m==Z)*(D.T in G.a)or(m==6)*W or(m==7)*q or(m==8)*(g(G.E,0))or(I!=None)*(m==9)or(m==10)*(U)or(m in[0,5])
T=(G.m if F else G.f)[m]
for _ in range(14):
 T=M(T,G.o[_],str(C[_]))
f=[G.H,u,b]
return T+N+(""if m else"".join([G.F[x]+", ".join([i.n for i in f[x]])+'"'if f[x]else""for x in[0,1,2]]))
</drac2>