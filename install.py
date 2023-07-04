# import launch
# import pkg_resources
import os

if 'CUDA_VISIBLE_DEVICES' in os.environ:
  print('Warning: Environment variable $ is set.')
else:
  print('Warning: Environment variable $ is not set.')
