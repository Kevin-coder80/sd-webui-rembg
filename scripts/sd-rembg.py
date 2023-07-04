from modules import scripts_postprocessing as sp
from modules.ui_components import FormRow
import gradio as gr
import rembg

modeles = [
  'None',
  'u2net', # 用于一般用例的预训练模型
  'u2netp', # u2net模型的轻量级版本
  'u2net_human_seg', # 用于人工分割的预训练模型
  'u2net_cloth_seg', # 从人类肖像中用于布料解析的预训练模型。这里的衣服被解析为3类：上半身，下半身和全身。
  'silueta', # 与u2net相同，但大小减少到43Mb
  'isnet-general-use', # 用于一般用例的新预训练模型
  'isnet-anime', # 动漫角色的高精度分割
  'sam' # 适用于任何用例的预训练模型
]

class Script():
  name = 'sd-rembg'
  model = None

  def ui( self ):
    with FormRow():
      model = gr.Dropdown( label='Remove BG (删除背景)', value="None", choices=modeles )
      mask = gr.Checkbox( label='Mask (返回遮罩)', value=False )
      invert_mask = gr.Checkbox( label='Invert Mask (反转遮罩)', value=False )
      alpha_cutout = gr.Checkbox( label='Alpha Cutout (Alpha抠图)', value=False )

    return {
      model,
      mask,
      invert_mask,
      alpha_cutout
    }

  def process(
    self,
    img: sp.PostprocessedImage,
    model,
    mask,
    invert_mask,
    alpha_cutout ):
    if model == 'None':
      return
