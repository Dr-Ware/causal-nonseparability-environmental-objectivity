# Causal Nonseparability and Environmental Objectivity

Reproducibility repository for the manuscript **Causal Nonseparability and Environmental Objectivity: Independence, Control-Assisted Records, and Quantum-Switch Benchmarks** by Scott Muniz.

## Release status

This repository is prepared for the initial archival release `v1.0.0`. This repository is publicly archived through GitHub releases and Zenodo.

## Repository map

- `manuscript/`: Version 5 DOCX and generated LaTeX source.
- `supplement/`: validation note and release-facing cover letter.
- `src/`: deterministic Python validation programs.
- `data/`: exact gate-level, reduced-normal-form, finite-shot, and interval-audit outputs.
- `figures/`: validation and circuit figures.
- `metadata/`: Zenodo and software metadata.
- `docs/`: release, clean-run, and DOI-update instructions.

## Quick reproduction

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/gate_level_validation_v4.py
python src/classical_validation_v3.py
python docs/verify_outputs.py
```

Both validation scripts write outputs to `/mnt/data` in the archived version. For a local clone, either run from a container with `/mnt/data` mapped to the repository root or change `OUT=Path('/mnt/data')` to `OUT=Path.cwd()` before execution. The frozen CSV/JSON files in `data/` are the release artifacts.

## Principal numerical results

- 51-point independent NumPy gate-level validation.
- Maximum analytic-formula error: `2.220446049250313e-16`.
- Maximum coherent-minus-best-fixed discrepancy: `2.220446049250313e-16`.
- 99 finite-shot ideal-sampling settings with 8,192 shots per pointer label.
- Mean absolute finite-shot error: `0.002457816104026167`.
- Conservative propagated interval inclusion on the frozen grid: `99/99`.

These are computational validation results, not physical-device measurements.

## Citation

Use `CITATION.cff`to cite this repository. The archived release is available at DOI: `10.5281/zenodo.21933737`.

## License

The Python software in this repository is made available under the MIT License. See the `LICENSE` file for the complete terms.