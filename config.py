"""Art-direction units only: NOT clinical dimensions or validated mechanics."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BLENDER_EXECUTABLE = '/Applications/Blender.app/Contents/MacOS/Blender'
ANIMATION_FPS = 30
DURATION_SECONDS = 27
CARDIAC_CYCLE_FRAMES = 72
RIGHT_ATRIUM_SCALE = (1.72, 1.40, 2.80)
RIGHT_VENTRICLE_SCALE = (1.94, 1.36, 3.65)
TRICUSPID_ANNULUS_DIAMETER = 2.32
FRAME_DIAMETER = 2.16
FRAME_HEIGHT = 0.96
FRAME_FLARE = 0.12
STRUT_RADIUS = 0.021
FRAME_CELLS = 18
LEAFLET_HEIGHT = 0.96
LEAFLET_WIDTH = 1.0
LEAFLET_THICKNESS = 0.012
OPENING_FRACTION = 0.80
BLOOD_PARTICLE_COUNT = 210
FLOW_SPEED = 1.0
REGURGITATION_PARTICLE_COUNT = 115
RENDER_WIDTH = 1920
RENDER_HEIGHT = 1080
RENDER_SAMPLES = 48
PREVIEW_WIDTH = 1280
PREVIEW_HEIGHT = 720
PREVIEW_SAMPLES = 12
REVEAL_START = 255
REVEAL_END = 315
END_CARD_START = 660
CAMERA_LENS = 52
CAMERA_CLIP_START = 0.05
CAMERA_CLIP_END = 200
CAMERAS = {
 'Hero_Camera': ((6.8,-12.5,8.2),(0,0,-0.25),52),
 'Right_Heart_Establishing': ((5.4,-14.3,6.4),(0,0,-0.3),49),
 'Native_TR_Closeup': ((3.7,-7.8,6.4),(0,0,-0.1),56),
 'Valve_Cutaway': ((3.5,-7.4,5.2),(0,0,-0.10),61),
 'Valve_Atrial_View': ((0.0,-2.4,8.8),(0,0,-0.1),56),
 'Valve_Ventricular_View': ((1.0,-4.2,-7.4),(0,0,-0.1),52),
}
# Neutral device has no delivery-system geometry. No real assets present at build.
IMPORTED_DEVICE = None  # project-relative OBJ/STL/PLY/FBX/GLB; STEP must be tessellated externally.
IMPORTED_DEVICE_SCALE = 1.0
