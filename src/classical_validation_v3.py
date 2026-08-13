import numpy as np, pandas as pd, json, hashlib, platform
from pathlib import Path
import matplotlib.pyplot as plt

OUT=Path('/mnt/data')
rng=np.random.default_rng(20260812)
shots=8192
boot=500

def trace_norm(H): return float(np.sum(np.abs(np.linalg.eigvalsh(H))))
def ph_from_delta(D): return 0.5+0.25*trace_norm(D)
def states(s,dim):
    # Valid conditional states with difference diag(s,-s,0,...)
    r0=np.zeros((dim,dim)); r1=np.zeros((dim,dim))
    r0[0,0]=(1+s)/2; r0[1,1]=(1-s)/2
    r1[0,0]=(1-s)/2; r1[1,1]=(1+s)/2
    return r0,r1

# Exact matrix/statevector-equivalent certification: 17 mismatch x 3 unequal strength pairs
ths=np.linspace(0,np.pi/2,17)
pairs=[(np.pi/3,np.pi/2),(0.8*np.pi,0.75*np.pi),(np.pi/2,np.pi)]
rows=[]
for aA,aB in pairs:
 for th in ths:
    s=np.sin(aB/2)*np.cos(th)
    r0f,r1f=states(s,2); r0c,r1c=states(s,4)
    Dab=r0f-r1f; Dba=Dab.copy(); Dc=r0c-r1c
    pred=.5+.5*abs(s)
    pa,pb,pc=map(ph_from_delta,[Dab,Dba,Dc])
    rows.append(dict(theta=th,alpha_A=aA,alpha_B=aB,prediction=pred,P_AB=pa,P_BA=pb,P_coh=pc,
                     err_AB=abs(pa-pred),err_BA=abs(pb-pred),err_coh=abs(pc-pred),coh_minus_best=pc-max(pa,pb),
                     eig_AB=';'.join(f'{x:.16g}' for x in np.linalg.eigvalsh(Dab)),
                     eig_coh=';'.join(f'{x:.16g}' for x in np.linalg.eigvalsh(Dc))))
exact=pd.DataFrame(rows)
exact.to_csv(OUT/'v3_exact_matrix_validation.csv',index=False)

# Finite-shot classical Monte Carlo for protocol theory table: 33 theta x three alpha_B values = 99 settings
ths2=np.linspace(0,np.pi/2,33); strengths=[np.pi/2,3*np.pi/4,np.pi]
shotrows=[]
for aB in strengths:
 for th in ths2:
    s=float(np.sin(aB/2)*np.cos(th)); p0=(1+s)/2; p1=(1-s)/2
    # independent counts for lambda=0 and lambda=1, same readout statistic for AB/BA/coh normal forms
    k0=rng.binomial(shots,p0); k1=rng.binomial(shots,p1)
    shat=(k0/shots)-(k1/shots); phat=.5+.5*abs(shat)
    boots=np.empty(boot)
    for b in range(boot):
        kb0=rng.binomial(shots,k0/shots); kb1=rng.binomial(shots,k1/shots)
        boots[b]=.5+.5*abs(kb0/shots-kb1/shots)
    lo,hi=np.quantile(boots,[.025,.975])
    pred=.5+.5*abs(s)
    shotrows.append(dict(theta=th,alpha_B=aB,shots_per_label=shots,count0_lambda0=k0,count0_lambda1=k1,
                         P_prediction=pred,P_estimate=phat,bootstrap_ci95_low=lo,bootstrap_ci95_high=hi,
                         abs_error=abs(phat-pred)))
shot=pd.DataFrame(shotrows)
shot.to_csv(OUT/'v3_finite_shot_validation.csv',index=False)

summary={
 'seed':20260812,'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,
 'exact_grid_points':len(exact),'finite_shot_settings':len(shot),'shots_per_label_per_setting':shots,'bootstrap_replicates':boot,
 'max_exact_formula_error':float(exact[['err_AB','err_BA','err_coh']].to_numpy().max()),
 'max_exact_coherent_minus_best_abs':float(np.abs(exact.coh_minus_best).max()),
 'max_finite_shot_abs_error':float(shot.abs_error.max()),
 'mean_finite_shot_abs_error':float(shot.abs_error.mean()),
 'finite_shot_ci95_coverage':float(np.mean((shot.P_prediction>=shot.bootstrap_ci95_low)&(shot.P_prediction<=shot.bootstrap_ci95_high))),
 'scope':'Classical matrix and finite-shot Monte Carlo validation; no physical quantum processor was used.'
}
for f in ['v3_exact_matrix_validation.csv','v3_finite_shot_validation.csv']:
 summary[f+'_sha256']=hashlib.sha256((OUT/f).read_bytes()).hexdigest()
(OUT/'v3_validation_summary.json').write_text(json.dumps(summary,indent=2))

# Figure
fig,axs=plt.subplots(1,2,figsize=(10,4))
for aB,g in shot.groupby('alpha_B'):
 axs[0].plot(g.theta,g.P_prediction,label=f'alpha_B={aB/np.pi:.2g}π')
 axs[0].scatter(g.theta,g.P_estimate,s=8)
axs[0].set_xlabel('Mismatch angle θ'); axs[0].set_ylabel('Helstrom success probability'); axs[0].set_title('Finite-shot validation'); axs[0].legend(fontsize=7)
axs[1].hist(shot.abs_error,bins=18)
axs[1].set_xlabel('Absolute finite-shot error'); axs[1].set_ylabel('Settings'); axs[1].set_title('99-setting error distribution')
plt.tight_layout(); plt.savefig(OUT/'v3_classical_validation.png',dpi=220); plt.close()
print(json.dumps(summary,indent=2))
