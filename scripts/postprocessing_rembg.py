from modules import scripts_postprocessing
from modules.ui_components import FormRow
from PIL import ImageOps, ImageColor
import gradio as gr
import rembg

models = [
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

class ScriptPostprocessingRembg(scripts_postprocessing.ScriptPostprocessing):
  name = "SD-Rembg"
  order = 10000
  model = None

  def ui( self ):
    with FormRow():
      model = gr.Dropdown( label='Remove BG 删除背景', value="None", choices=models )
      mask = gr.Checkbox( label='Mask 返回遮罩', value=False )
      invert_mask = gr.Checkbox( label='Invert Mask 反转遮罩', value=False )
      alpha_cutout = gr.Checkbox( label='Alpha Cutout 抠图', value=False )

    with FormRow():
      background_color = gr.ColorPicker( label="Background color 背景颜色", default=(0, 0, 0) )

    with FormRow():
      background_opacity = gr.Slider( label="Background opacity 背景透明", minimum=0, maximum=255, step=1, value=0 )

    with FormRow(visible=False) as alpha_mask_row:
      alpha_cutout_erode_size = gr.Slider(label="Erode size（侵蚀大小）", minimum=0, maximum=40, step=1, value=10)
      alpha_cutout_foreground_threshold = gr.Slider(label="Foreground threshold（前景阈值）", minimum=0, maximum=255, step=1, value=240)
      alpha_cutout_background_threshold = gr.Slider(label="Background threshold（背景阈值）", minimum=0, maximum=255, step=1, value=10)

    alpha_cutout.change(
        fn=lambda x: gr.update(visible=x),
        inputs=[alpha_cutout],
        outputs=[alpha_mask_row],
    )

    return {
      'rembg_model': model,
      'rembg_mask': mask,
      'rembg_invert_mask': invert_mask,
      'rembg_alpha_cutout': alpha_cutout,
      'background_color': background_color,
      'background_opacity': background_opacity,
      'alpha_cutout_erode_size': alpha_cutout_erode_size,
      'alpha_cutout_foreground_threshold': alpha_cutout_foreground_threshold,
      'alpha_cutout_background_threshold': alpha_cutout_background_threshold,
    }

  def process(
    self,
    img: scripts_postprocessing.PostprocessedImage,
    rembg_model,
    rembg_mask,
    rembg_invert_mask,
    rembg_alpha_cutout,
    background_color,
    background_opacity,
    alpha_cutout_foreground_threshold,
    alpha_cutout_background_threshold,
    alpha_cutout_erode_size ):
    if rembg_model == "None":
      return

    background_color = ImageColor.getcolor(background_color, "RGB")
    background_color = (*background_color, background_opacity)

    img.image = rembg.remove(
      img.image,
      session=rembg.new_session(rembg_model),
      only_mask=rembg_mask,
      alpha_matting=rembg_alpha_cutout,
      bgcolor=background_color,
      alpha_matting_foreground_threshold=alpha_cutout_foreground_threshold,
      alpha_matting_background_threshold=alpha_cutout_background_threshold,
      alpha_matting_erode_size=alpha_cutout_erode_size,
    )

    if rembg_mask and rembg_invert_mask:
      img.image = ImageOps.invert(img.image)

    img.info['Rembg'] = rembg_model
