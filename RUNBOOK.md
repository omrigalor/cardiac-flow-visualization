# Exact commands
Enter the existing project (do not create another nested directory):
```sh
cd /Users/omrigalor/Desktop/concept_medical_animation
```
Locate / verify Blender:
```sh
command -v blender
ls /Applications/Blender.app/Contents/MacOS/Blender
/Applications/Blender.app/Contents/MacOS/Blender --background --factory-startup --python-expr "import bpy; print(bpy.app.version_string)"
```
Blender background startup needs the already approved executable permission outside the Codex sandbox. Do not combine filesystem heredocs with Blender commands in one escalated command; keep code edits separate from execution so the saved executable permission applies.

Rebuild / validate:
```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python blender/build_project.py
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/validation.py
```
Open the saved project, or start a live viewer (use only one):
```sh
/Applications/Blender.app/Contents/MacOS/Blender valve_concept.blend
/Applications/Blender.app/Contents/MacOS/Blender --python blender/live_view.py
```
Diagnostics / short animated segment / complete 27-second 720p preview:
```sh
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode diagnostics
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode segment
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode preview
```
Higher-quality stills and final 1080p sequence:
```sh
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode stills
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode final --engine BLENDER_EEVEE
```
Omit `--engine BLENDER_EEVEE` for Cycles final. `--start N --end M` selects a range. Existing PNGs are skipped. Archive old frames before a changed-scene rerender; do not mix revisions.

Generate separate cards / encode (project-local FFmpeg is installed):
```sh
python3 blender/make_endcards.py
.tools/venv/bin/python blender/encode.py --source renders/previews/segment --start 361 --output renders/previews/function_segment.mp4 --no-endcard
.tools/venv/bin/python blender/encode.py --source renders/previews/preview --output renders/previews/concept_preview.mp4
.tools/venv/bin/python blender/encode.py --source renders/frames --output renders/final/concept_presentation.mp4
.tools/venv/bin/python blender/encode.py --source renders/frames --output renders/final/concept_internal_concept.mp4 --internal
```

Resume after a usage reset:
“Read PROGRESS.md and RUNBOOK.md, inspect the existing project and latest renders, and continue from where the previous session stopped. Preserve the stable anterior treatment camera followed by one slow 360-degree X-axis hero orbit, whole-heart opening, cellular blood flow, separate end card, and correct tricuspid physiology. Complete and visually verify the pending video deliverables. Do not claim photorealism or validated simulation.”

Render interruption: create `renders/STOP_RENDER` to request a graceful stop after the current frame; remove it before resuming. Generated PNGs are preserved.

Finalize PNG end card and Desktop delivery after rendering/encoding:
```sh
python3 blender/finish_exports.py --cards
.tools/venv/bin/python blender/encode.py --source renders/frames --output renders/final/concept_presentation.mp4 --no-endcard
.tools/venv/bin/python blender/encode.py --source renders/frames --output renders/final/concept_internal_concept.mp4 --internal
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/prepare_delivery.py
python3 blender/finish_exports.py --copy
```
The Desktop copy operation is explicitly authorized by the user. Both copies are SHA-256 checked.

Current delivered video is 720p. Optional 1080p resume (only in a future authorized session):
```sh
mv renders/frames renders/frames_720
mv renders/frames_1080_partial renders/frames
/Applications/Blender.app/Contents/MacOS/Blender --background valve_concept.blend --python blender/render.py -- --mode final --engine BLENDER_EEVEE --start 148 --end 810
python3 blender/finish_exports.py --cards
```
Do not rerender into the 720p directory; keep frame dimensions consistent.

Verify the delivered 720p sequence: `python3 blender/verify_outputs.py --folder renders/frames --end 900`.
