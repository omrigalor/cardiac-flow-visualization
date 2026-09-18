# Procedural Cardiac Anatomy & Flow Visualization

A locally reproducible 3D medical visualization pipeline, built in Blender and driven entirely
from Python. It generates right-heart anatomy from a public reference atlas, animates the
tricuspid valve through the cardiac cycle, illustrates regurgitant flow, and renders a
controlled anatomical orbit — deterministically, from scripts, with no manual modelling.

## What it does

- **Anatomy from a public atlas.** Myocardial geometry is adapted from the Human Reference
  Atlas / NLM Visible Human dataset (CC BY 4.0), then registered, smoothed and cut for
  presentation. Great-vessel context is generated procedurally.
- **Valve motion on a real cardiac timeline.** Leaflet opening and coaptation follow the
  cardiac cycle — predominantly diastolic filling, closure through 0.48–0.62 of the cycle,
  systole to 0.90 — rather than an arbitrary loop.
- **Flow illustration.** Forward flow right atrium → right ventricle in ventricular diastole;
  regurgitation right ventricle → right atrium in systole only.
- **A deterministic render pipeline.** Scene construction, cameras, lighting, materials,
  animation, validation and encoding are separate modules, all reproducible from `config.py`.
- **Self-validation.** `validation.py`, `orbit_diagnostics.py`, `benchmark_geometry.py` and
  `verify_outputs.py` check the scene before it renders rather than after it looks wrong.

## What this is not

This is **illustrative, not computationally validated**. It is not CFD, not FEA, not fatigue or
structural mechanics, not hemodynamics, not a clinical prediction, and not a regulatory
simulation. Cell size and spacing are exaggerated for visibility. The visual contrast between
untreated and treated states is a presentation device, not a measured efficacy claim.

No proprietary or patient-specific geometry is included. Device geometry, client branding and
delivered footage are deliberately excluded from this repository; what remains is the anatomy
and rendering engineering.

## Layout

| Path | What it is |
|---|---|
| `config.py` | Every art and geometry parameter in one place |
| `blender/` | Scene generation, animation, cameras, lighting, render, validation |
| `geometry/` | Registration metadata for the reference anatomy |
| `simulation/` | Flow interfaces and sample data |
| `docs/` | Attribution and method notes |
| `RUNBOOK.md` | How to reproduce a render end to end |

## Attribution

Source myocardium adapted from the Human Reference Atlas / NLM Visible Human dataset under
CC BY 4.0 — see `docs/ATTRIBUTION.md`. Registered and smoothed for presentation, not for
patient-specific planning.
