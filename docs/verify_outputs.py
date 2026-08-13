import json, pandas as pd
from pathlib import Path
R=Path(__file__).resolve().parents[1]
g=pd.read_csv(R/'data/v4_gate_level_validation.csv')
s=pd.read_csv(R/'data/v4_finite_shot_validation.csv')
j=json.loads((R/'data/v4_validation_summary.json').read_text())
assert len(g)==51 and len(s)==99
assert abs(g[['err_AB','err_BA','err_COH']].to_numpy()).max() <= 3e-16
assert abs(g['coh_minus_best']).max() <= 3e-16
assert bool(s['covered'].all())
assert j['gate_grid_points']==51 and j['finite_shot_settings']==99
print('PASS: frozen outputs match the manuscript-level validation counts and tolerances.')
