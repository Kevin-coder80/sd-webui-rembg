import launch
# import pkg_resources
import os

rembg_version = '2.0.49'

if 'CUDA_VISIBLE_DEVICES' in os.environ:
  print('Warning: Environment variable $ is set.')
  if not launch.is_installed('rembg[gpu]'):
    launch.run_pip(f"install rembg[gpu]=={rembg_version} --no-deps",  f"rembg {rembg_version} with GPU support")

  if not launch.is_installed('onnxruntime-gpu'):
    launch.run_pip(f"install onnxruntime-gpu")
else:
  if not launch.is_installed('rembg'):
    launch.run_pip(f"install rembg=={rembg_version} --no-deps",  f"rembg {rembg_version} without GPU support")

  if not launch.is_installed('onnxruntime'):
    launch.run_pip(f"install onnxruntime")

for dep in ['pymatting', 'pooch']:
  if not launch.is_installed(dep):
    launch.run_pip( f"install {dep}", f"{dep} is extension for rembg." )
