import os
import utils.generate as g
from typing import List, Dict


POSES = [[0.15, 0.0, 0.0],
         [0.0, 0.25, 0.0],
         [-0.15, 0.0, 0.0],
         [0.0, -0.25, 0.0],
         [0.15, 0.25, 0.0],
         [0.15, -0.25, 0.0],
         [-0.15, 0.25, 0.0],
         [-0.15, -0.25, 0.0]]

ILLUMINATIONS = [[0.25, 0.0, 1.0],
                 [0.0, 0.25, 1.0],
                 [-0.25, 0.0, 1.0],
                 [0.0, -0.25, 1.0],
                 [0.25, 0.25, 1.0],
                 [0.25, -0.25, 1.0],
                 [-0.25, 0.25, 1.0],
                 [-0.25, -0.25, 1.0]]


def generate_batch_on_pose(batchname: str, params: Dict[str, str]) -> List[str]:

    random = params.get('random')
    race = params.get('race')
    gender = params.get('gender')

    head_model = params.get('head_model')
    mouth_model = params.get('mouth_model')
    hair_model = params.get('hair_model')
    hair_color = params.get('hair_color')

    os.mkdir(batchname)
    imgs = []

    g.init_face(os.path.join(batchname, batchname), random, race, gender)
    g.change_face_params(os.path.join(batchname, batchname), os.path.join(batchname, batchname), 'caricatureshape', '0.01')
    g.construct_face_models(os.path.join(batchname, batchname), head_model,
                          mouth_model, hair_model, hair_color)
    g.add_expression_to_models(os.path.join(batchname, batchname), 'SmileOpen', 0.5)
    g.render_model_to_png(os.path.join(batchname, batchname))
    os.rename(os.path.join(batchname, batchname+'Render.png'),
              os.path.join(batchname, batchname+'Render_pose_0.png'))
    for idx, pose in enumerate(POSES):
        g.change_pose(os.path.join(batchname, batchname+'Render'), pose)
        g.render_renderer(os.path.join(batchname, batchname+'Render'))
        os.rename(os.path.join(batchname, batchname+'Render.png'),
                  os.path.join(batchname, batchname+'Render_pose_'+str(idx+1)+'.png'))
        imgs.append(batchname+'Render_pose_'+str(idx+1)+'.png')

    return imgs


def generate_batch_on_illumination(batchname: str, params: Dict[str, str]) -> List[str]:

    random = params.get('random')
    race = params.get('race')
    gender = params.get('gender')

    head_model = params.get('head_model')
    mouth_model = params.get('mouth_model')
    hair_model = params.get('hair_model')
    hair_color = params.get('hair_color')

    os.mkdir(batchname)
    imgs = []

    g.init_face(os.path.join(batchname, batchname), random, race, gender)
    g.construct_face_models(os.path.join(batchname, batchname), head_model,
                          mouth_model, hair_model, hair_color)
    g.add_expression_to_models(os.path.join(batchname, batchname), 'SmileOpen', 0.5)
    g.render_model_to_png(os.path.join(batchname, batchname))
    os.rename(os.path.join(batchname, batchname+'Render.png'),
              os.path.join(batchname, batchname+'Render_illum_0.png'))
    for idx, illum in enumerate(ILLUMINATIONS):
        g.change_illumination(os.path.join(batchname, batchname+'Render'), illum)
        g.render_renderer(os.path.join(batchname, batchname+'Render'))
        os.rename(os.path.join(batchname, batchname+'Render.png'),
                  os.path.join(batchname, batchname+'Render_illum_'+str(idx+1)+'.png'))
        imgs.append(batchname+'Render_illum_'+str(idx+1)+'.png')

    return imgs


if __name__=='__main__':

    params = {
                'gender': 'male',
                'race': 'eastAsian'
             }

    generate_batch_on_pose('mofii', params)
    # generate_batch_on_illumination('mofiiillum', params)
    
