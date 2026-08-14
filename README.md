# Causal Nonseparability and Environmental Objectivity

This repository supports the manuscript:

**Causal Nonseparability and Environmental Objectivity: Independence, Control-Assisted Records, and Quantum-Switch Benchmarks**

The central result is a logical-independence framework connecting two active areas of quantum information science: environmental objectivity, as studied in Quantum Darwinism and spectrum-broadcast structure, and causal nonseparability, as studied in process-matrix and quantum-switch frameworks.

The manuscript shows that environmental objectivity and causal nonseparability are independent operational structures. A process may possess redundant environmental records without being causally nonseparable, and a causally nonseparable process need not generate objective environmental records. Control-assisted information can appear in joint access to the order control and an environmental fragment, but that contribution is bounded, task dependent, and access dependent.

## Release status

This repository is prepared for the initial archival release `v1.0.2`. This repository is publicly archived through GitHub releases and Zenodo.

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

Use `CITATION.cff`to cite this repository. The archived release is available at DOI: `10.5281/zenodo.21936044`.

## License

The Python software in this repository is made available under the MIT License. See the `LICENSE` file for the complete terms.

## Public archive

- GitHub repository: https://github.com/Dr-Ware/causal-nonseparability-environmental-objectivity
- Zenodo record: https://zenodo.org/records/21933737
- DOI: 10.5281/zenodo.21936044
- Manuscript version supported: Version 6
- Archive version: v1.0.2 or current release tag used for the DOI

## Comparator hierarchy

The manuscript reports a resource-matched joint-access Holevo advantage. This is not claimed to be an optimization over the full causally separable process cone.

| Comparator level | Used in manuscript? | Role | Claim status |
|---|---:|---|---|
| Fixed AB order | Yes | Baseline definite order | Directly computed |
| Fixed BA order | Yes | Opposite definite-order baseline | Directly computed |
| Optimized fixed-order mixture | For environment-only access | Checks whether discarded control reduces to a mixture | No fragment-only advantage found in declared tests |
| Resource-matched controlled/fixed family | Yes | Main fair comparator | Joint-access Holevo advantage reported |
| Full causally separable cone | No | Global process-level comparator | Outside scope |

## AI assistance disclosure

Microsoft 365 Copilot assisted with language editing, code review, bibliographic organization, consistency analysis, and draft preparation. All mathematical derivations, numerical outputs, references, and scientific claims were independently verified by the author. No AI system is an author.