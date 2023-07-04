import launch
# import pkg_resources
import os

if 'CUDA_VISIBLE_DEVICES' in os.environ:
  print('Warning: Environment variable $ is set.')
  if not launch.is_installed('rembg[gpu]'):
    launch.run_pip.install('rembg[gpu]')

  if not launch.is_installed('onnxruntime-gpu'):
    launch.run_pip.install('onnxruntime-gpu')
else:
  print('Warning: Environment variable $ is not set.')
  if not launch.is_installed('rembg'):
    launch.run_pip.install('rembg')

  if not launch.is_installed('onnxruntime'):
    launch.run_pip.install('onnxruntime')
