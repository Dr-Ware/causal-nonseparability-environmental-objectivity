import numpy as np, pandas as pd, json, hashlib, platform
from pathlib import Path
from scipy.stats import beta
import matplotlib.pyplot as plt

OUT=Path('/mnt/data'); rng=np.random.default_rng(20260812)
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex); H=np.array([[1,1],[1,-1]],complex)/np.sqrt(2)
P0=np.diag([1,0]).astype(complex); P1=np.diag([0,1]).astype(complex)
def ry(a): return np.array([[np.cos(a/2),-np.sin(a/2)],[np.sin(a/2),np.cos(a/2)]],complex)
def kron4(a,b,c,d): return np.kron(np.kron(np.kron(a,b),c),d)
def one(g,q):
 ops=[I,I,I,I]; ops[q]=g; return kron4(*ops)
def controlled_ry(ctrl,target,a):
 ops0=[I,I,I,I]; ops1=[I,I,I,I]; ops0[ctrl]=P0; ops1[ctrl]=P1; ops1[target]=ry(a)
 return kron4(*ops0)+kron4(*ops1)
def A(a): return controlled_ry(1,2,a)
def B(th,a): return one(ry(-th),1) @ controlled_ry(1,3,a) @ one(ry(th),1)
def ptrace_pure(psi,keep):
 arr=psi.reshape([2]*4); trace=[q for q in range(4) if q not in keep]
 # move keep first, trace last
 perm=keep+trace; m=np.transpose(arr,perm).reshape(2**len(keep),2**len(trace))
 return m@m.conj().T
def state(arm,lam,th,aA,aB):
 base=np.zeros(16,complex); idx=(0<<3)|(lam<<2)|(0<<1)|0; base[idx]=1
 UA,UB=A(aA),B(th,aB)
 if arm=='AB': return UB@UA@base
 if arm=='BA': return UA@UB@base
 plus=one(H,0)@base
 Uab=UB@UA; Uba=UA@UB
 U=P0[0,0]*0 # dummy
 # block-control on T: T=0 AB, T=1 BA
 C=kron4(P0,I,I,I)@Uab + kron4(P1,I,I,I)@Uba
 return C@plus
def hel(r0,r1): return .5+.25*np.sum(np.abs(np.linalg.eigvalsh((r0-r1+(r0-r1).conj().T)/2)))
def matstr(M): return ';'.join(','.join(f'{z.real:.16g}{z.imag:+.16g}j' for z in row) for row in M)

rows=[]
for th in np.linspace(0,np.pi/2,17):
 for aA,aB in [(np.pi,np.pi),(np.pi/2,3*np.pi/4),(2.2,2.7)]:
  r={}
  for arm in ['AB','BA','COH']:
   keep=[3] if arm!='COH' else [0,3]
   r[arm]=[ptrace_pure(state(arm,l,th,aA,aB),keep) for l in [0,1]]
  D={k:v[0]-v[1] for k,v in r.items()}
  pred=.5+.5*abs(np.sin(aB/2)*np.cos(th))
  ph={k:hel(*v) for k,v in r.items()}
  rows.append(dict(theta=th,alpha_A=aA,alpha_B=aB,PH_AB=ph['AB'],PH_BA=ph['BA'],PH_COH=ph['COH'],PH_analytic=pred,
   err_AB=abs(ph['AB']-pred),err_BA=abs(ph['BA']-pred),err_COH=abs(ph['COH']-pred),coh_minus_best=ph['COH']-max(ph['AB'],ph['BA']),
   eig_AB=';'.join(f'{x:.16g}' for x in np.linalg.eigvalsh(D['AB'])),eig_BA=';'.join(f'{x:.16g}' for x in np.linalg.eigvalsh(D['BA'])),eig_COH=';'.join(f'{x:.16g}' for x in np.linalg.eigvalsh(D['COH'])),
   matrix_AB=matstr(D['AB']),matrix_BA=matstr(D['BA']),matrix_COH=matstr(D['COH'])))
gate=pd.DataFrame(rows); gate.to_csv(OUT/'v4_gate_level_validation.csv',index=False)

# Finite-shot study with conservative simultaneous Clopper-Pearson intervals
shots=8192; reps=2000; alphas=[np.pi/2,3*np.pi/4,np.pi]; ths=np.linspace(0,np.pi/2,33)
def cp(k,n,alpha):
 lo=0 if k==0 else beta.ppf(alpha/2,k,n-k+1); hi=1 if k==n else beta.ppf(1-alpha/2,k+1,n-k); return lo,hi
srows=[]
for aB in alphas:
 for th in ths:
  sval=float(np.sin(aB/2)*np.cos(th)); p0=(1+sval)/2; p1=(1-sval)/2
  k0=rng.binomial(shots,p0); k1=rng.binomial(shots,p1)
  d=abs(k0/shots-k1/shots); pest=.5+.5*d; pred=.5+.5*abs(sval)
  # Bonferroni simultaneous 95%: each binomial CI at 97.5%
  l0,u0=cp(k0,shots,.025); l1,u1=cp(k1,shots,.025)
  dmax=max(abs(l0-u1),abs(u0-l1)); dmin=0 if not (u0<l1 or u1<l0) else min(abs(u0-l1),abs(u1-l0))
  lo=.5+.5*dmin; hi=.5+.5*dmax
  srows.append(dict(theta=th,alpha_B=aB,shots_per_label=shots,count0_lambda0=k0,count0_lambda1=k1,P_prediction=pred,P_estimate=pest,simultaneous_CP95_low=lo,simultaneous_CP95_high=hi,bias=pest-pred,abs_error=abs(pest-pred),covered=lo<=pred<=hi))
shot=pd.DataFrame(srows); shot.to_csv(OUT/'v4_finite_shot_validation.csv',index=False)
# Identify misses and boundary clustering
miss=shot[~shot.covered].copy(); miss.to_csv(OUT/'v4_interval_noncoverage.csv',index=False)
summary={'seed':20260812,'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,
'gate_grid_points':len(gate),'max_gate_formula_error':float(gate[['err_AB','err_BA','err_COH']].to_numpy().max()),'max_gate_coherent_minus_best_abs':float(np.abs(gate.coh_minus_best).max()),
'finite_shot_settings':len(shot),'shots_per_label':shots,'interval_method':'Bonferroni simultaneous Clopper-Pearson intervals for p0 and p1, propagated through |p0-p1|','interval_coverage':float(shot.covered.mean()),'noncoverage_count':int((~shot.covered).sum()),
'mean_bias':float(shot.bias.mean()),'max_abs_bias':float(np.abs(shot.bias).max()),'mean_abs_error':float(shot.abs_error.mean()),'max_abs_error':float(shot.abs_error.max()),
'finite_shot_scope':'Ideal projective sampling only; excludes gate error, decoherence, readout bias, crosstalk, compilation overhead, and calibration drift.'}
for f in ['gate_level_validation_v4.py','v4_gate_level_validation.csv','v4_finite_shot_validation.csv','v4_interval_noncoverage.csv']:
 summary[f+'_sha256']=hashlib.sha256((OUT/f).read_bytes()).hexdigest()
(OUT/'v4_validation_summary.json').write_text(json.dumps(summary,indent=2)); summary['v4_validation_summary.json_sha256']=hashlib.sha256((OUT/'v4_validation_summary.json').read_bytes()).hexdigest()
(OUT/'v4_checksums.sha256').write_text('\n'.join(f'{hashlib.sha256((OUT/f).read_bytes()).hexdigest()}  {f}' for f in ['gate_level_validation_v4.py','v4_gate_level_validation.csv','v4_finite_shot_validation.csv','v4_interval_noncoverage.csv','v4_validation_summary.json']))
# Figure with representative error bars
fig,axs=plt.subplots(1,2,figsize=(10,4.2))
for aB,g in shot.groupby('alpha_B'):
 yerr=np.vstack([g.P_estimate-g.simultaneous_CP95_low,g.simultaneous_CP95_high-g.P_estimate])
 axs[0].plot(g.theta,g.P_prediction,label=f'αB={aB/np.pi:.2g}π')
 sel=np.arange(0,len(g),4); axs[0].errorbar(g.theta.iloc[sel],g.P_estimate.iloc[sel],yerr=yerr[:,sel],fmt='o',ms=3,capsize=2)
axs[0].axvline(np.pi/2,color='gray',ls=':',lw=1); axs[0].set(xlabel='Mismatch angle θ',ylabel='Helstrom success probability',title='Gate formula and finite-shot estimates'); axs[0].legend(fontsize=7)
axs[1].scatter(shot.theta,shot.bias,c=shot.alpha_B,cmap='viridis',s=16); axs[1].axhline(0,color='black',lw=.8); axs[1].axvline(np.pi/2,color='gray',ls=':',lw=1); axs[1].set(xlabel='Mismatch angle θ',ylabel='Finite-shot bias',title='Bias across 99 ideal-sampling settings')
plt.tight_layout(); plt.savefig(OUT/'v4_validation_figure.png',dpi=220); plt.close()
print(json.dumps(summary,indent=2))
