# Cardiac Concept — Tricuspid Valve Replacement
A locally reproducible 3D concept visualization for an investor/physician presentation. The 30-second film begins with the exterior heart, reveals an anterior right-heart cutaway, illustrates native tricuspid regurgitation, reveals a neutral conceptual replacement, and shows its function. A single controlled 360-degree anatomical-X orbit closes the 27-second medical sequence, followed by a 3-second separate end card. Branding is on a separate end card, never over the anatomy.

## Accuracy and limitations
The current flow and mechanical motion are illustrative rather than computationally validated. This is **not** validated CFD, FEA, fatigue, structural mechanics, hemodynamics, a clinical prediction, or a regulatory simulation. The procedural device is **not the device proprietary CAD** and no quantitative clinical or current regulatory claims are included.
The source myocardium is adapted from the Human Reference Atlas / NLM Visible Human dataset under CC BY 4.0; see [attribution](docs/ATTRIBUTION.md). Source geometry is registered, smoothed and cut for presentation, not patient-specific planning. Supplemental great-vessel context is procedural. Cell size and spacing are exaggerated for visibility.

Forward flow: right atrium → right ventricle in ventricular diastole. Leaflets coapt in ventricular systole. Untreated regurgitation: RV → RA in systole only. The treated visualization suppresses the illustrative regurgitant stream. This visual contrast is not a measured efficacy claim.

## Open the video
Open **WATCH_VIDEO.mp4** directly in this folder. This is the main presentation video: 30 seconds, 1280×720, 30 fps. Open **valve_concept.blend** to explore the animated scene. Both are also copied directly to Desktop. The optional 1080p render was stopped at the user’s request to conserve usage; six full-HD stills are available.

## Main deliverables
The finished watchable MP4 and navigable Blender scene are copied directly to Desktop as `the device_Medical_Animation.mp4` and `the device_Medical_Animation.blend`. Project originals remain below. See PROGRESS.md for completion status.

## Files
- `valve_concept.blend`: complete saved Blender project.
- `config.py`: central art parameters. All geometry dimensions are visualization units.
- `blender/`: deterministic scene generation, animation, render and validation scripts.
- `assets/reference/`: HRA anatomy and user-provided historical reference movie (not reused footage).
- `assets/branding/`: separate clean/internal end cards; text branding, no invented logo.
- `renders/diagnostics/`: geometry/phase checks and validation JSON.
- `renders/previews/`: preview PNGs, short segment and full preview MP4.
- `renders/stills/`: higher-quality Cycles stills.
- `renders/frames/`: final PNG sequence, excluded from Git.
- `renders/final/`: presentation and internal H.264 exports.
- `geometry/imported/`: future verified device geometry.
- `simulation/interfaces/`: documented future CFD/FEA/displacement contracts, no fabricated data.

## Build / view / render
Exact commands are in [RUNBOOK.md](RUNBOOK.md). Blender 5.2.1 is verified at `/Applications/Blender.app/Contents/MacOS/Blender`.

```sh
cd /Users/omrigalor/Desktop/concept_medical_animation
/Applications/Blender.app/Contents/MacOS/Blender --background --python blender/build_project.py
/Applications/Blender.app/Contents/MacOS/Blender valve_concept.blend
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode preview
```

The interactive live viewer (`blender/live_view.py`) reloads saved builds and plays the timeline. Only one GUI viewer is needed; background render processes may temporarily add macOS Dock icons.

Change central parameters in `config.py`, then rebuild. The `.blend` is saved at each major milestone. Preview uses Eevee. Final/stills default to Cycles; `--engine BLENDER_EEVEE` supports faster full-HD delivery. PNG renders resume by skipping existing files; use a new output folder or archive previous frames when scene content changes.

## Real geometry and computational upgrades
See `geometry/imported/README.md`. The annulus coordinate system is origin (0,0,0), RA=+Z and RV=-Z. STL/OBJ/PLY/FBX/GLB adapters are provided in `blender/import_device.py`; STEP needs external tessellation. Importing CAD does not automatically provide physically valid leaflet mechanics. Preserve the heart/cameras/lights/controller while replacing procedural frame/skirt and registering real leaflet topology.
See `simulation/README.md`. CFD, FEA and displacement interfaces currently raise NotImplementedError intentionally. Real fields require provenance, units, coordinate transforms, persistent node IDs, topology checks and time registration before visualization.

## Visual status
See `PROGRESS.md` for current delivered files, visual limitations and the next task. A successful sanity report is not anatomical or clinical certification. The requested near-photographic quality target is assessed visually; it is not guaranteed by the render engine or mesh source.

Local Git only; no remote push. Generated videos, frame caches and `.blend` backups are excluded from commits. The main `.blend` remains on disk and is regenerable from the committed source.
