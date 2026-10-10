# Tafelmacher’s parabola in proportional arithmetic — reproducible figures

Companion code for the Classroom Note **Beyond the Classical Parabola: Tafelmacher’s Construction in Proportional Arithmetic**, by William Campillay-Llanos and Noemí Cárcamo-Mansilla.

## Contents

- `tafelmacher_figures.py`: source for the classical/proportional Tafelmacher construction (Figure 2) and exact tangencies (Figure 4).
- `figures/`: PNG outputs of the script.
- `requirements.txt`: Python dependencies.

**Coverage:** This initial repository release reproduces Figures 2 and 4 only. Figures 1 and 3 have not yet been included as reproducible scripts; do not claim this release reproduces all four manuscript figures.

## Reproduce

```bash
python -m pip install -r requirements.txt
python tafelmacher_figures.py
```

The script writes `figure2_tafelmacher_PYTHON.png` and `figure4_tangency_PYTHON.png` into the current working directory. It also runs numerical checks of incidence and tangency.

## Mathematics

Ordinary tangent family:

`h(1-2t)x + ay = ah(1-2t+2t^2)`.

Contact point: `T(t) = (a(1-2t), 2ht(1-t))`.

Parabola: `y = (h/2)(1-x^2/a^2)`.

Proportional operations on positive real numbers are explicitly implemented in the Python script: `padd`, `psub`, `pmul`, `pdiv`, `pscalar`, `pinterp` and `psquare`. Logarithms are used internally to implement the field operations and to verify the field isomorphism, not to define the proportional parabola.

## Citation and archive

Archive this repository in Zenodo to obtain a DOI, then cite the **actual DOI assigned by Zenodo** in the manuscript. No DOI has yet been assigned to this package.

## Funding

ANID FONDECYT Project No. 11261185 (as reported by the authors).
