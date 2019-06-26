import re
import os
import subprocess as sp
from typing import List, Dict
from xml.etree import ElementTree as ET


FG_SDK_PATH = '/Users/mofii/Documents/workplace/facegen'
FG_ANIMATE_PATH = os.path.join(FG_SDK_PATH, 'data/csam/Animate')
FG_HEAD_PATH = os.path.join(FG_ANIMATE_PATH, 'Head')
FG_MOUTH_PATH = os.path.join(FG_ANIMATE_PATH, 'Head')
FG_HAIR_PATH = os.path.join(FG_ANIMATE_PATH, 'Hair')


def init_face(filename: str, random: str, race: str, gender: str):
    
    '''Init a face model with parameters

    Parameters:
    filename (str):     filename for .fg face model
    random (str):       face domain, default 'random'
                            [ random | average ]
    race (str):         race param of the face, default 'any'
                            [ african | european | eastAsian | southAsian | any ]
    gender (str):       gender param of the face, default 'any'
                            [ male | female | any ]

    Return:
        (boolean):      True if the model is initialized, False otherwise
    '''

    # ----------------------------------------------------------------
    # This is an Python API for FaceGen. While FaceGen requires all
    # command line parameters, we allow users to generate face/model
    # with default values. This is why the default value declarations
    # are explictly written for most functions in this program.
    # ----------------------------------------------------------------

    # default value for random is 'random'
    if random is None:
        random = 'random'

    # default value for race is 'any'
    if race is None:
        race = 'any'

    # default value for gender is 'any'
    if gender is None:
        gender = 'any'

    # Generate a random face:
    #     $ fg3 random any any <filename>.fg
    params = ['fg3', 'create', random, race, gender, filename+'.fg']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False

    return True


def get_face_params(filename: str):

    '''Get the params of a given .fg face model

    Parameters:
    filename (str): filename of the target face model

    Return:
    params (list[str]): a list of face params
                            [<age>, <gender>, <caricature shape>, <caricature color>,
                            <asymmetry>, <african>, <east asian>, <south asian>,
                            <european>]
    '''
    
    # Get face params of a given face model
    #     $ fg3 controls demographic edit <filename>.fg
    params = ['fg3', 'controls', 'demographic', 'edit', filename+'.fg']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return None
    else:
        params = re.split('\s', stdout)
        # remove parameter names from the list
        idx = [16, 14, 12, 10, 8, 6, 4, 2, 0]
        for i in idx:
            params.pop(i)
        return params


def change_face_params(filename: str, newfilename: str, param: str, value: str) -> bool:

    '''Change the params of a given .fg face model

    Parameters:
    filename (str):     filename of the target face model
    newfilename (str):  filename of the new face model
    param (str):        the param name to be changed
    value (str):        the target value of the chosen param

    Return:
        (boolean):      True if the param is changed, False otherwise
    '''
    
    # Change the face params of a given face model
    #     $ fg3 controls demographic edit <filename>.fg <param> <value> <newfilename>.fg
    params = ['fg3', 'controls', 'demographic', 'edit', filename+'.fg', param, value, newfilename+'.fg']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False
    return True


def construct_face_models(filename: str, head_model: str,
                          mouth_model: str, hair_model: str,
                          hair_color: str) -> bool:

    '''Construct face models: head, mouth, hair, and copy hair color maps

    Parameters:
    filename (str):     filename of the selected face model
    head_model (str):   the head model in the directory <FG_HEAD_PATH>, default 'HeadHires'
    mouth_model (str):  the mouth model in the directory <FG_MOUTH_PATH>, default 'Mouth'
    hair_model (str):   the hair model in the directory <FG_HAIR_PATH>, default 'MidlengthStraight'
    hair_color (str):   the color of the hair model in the directory <FG_HAIR_PATH>, default 'MidlengthStraight_Brown'

    Return:
        (boolean):      True if models are constructed, False otherwise
    '''

    # default value for head_model is 'HeadHire'
    if head_model is None:
        head_model = 'HeadHires'

    # default value for mouth_model is 'Mouth'
    if mouth_model is None:
        mouth_model = 'Mouth'

    # default value for hair_model is 'MidLengthStraight'
    if hair_model is None:
        hair_model = 'MidlengthStraight'

    # default value for hair_model_color is 'MidlengthStraight_Brown'
    if hair_color is None:
        hair_color = 'MidlengthStraight_Brown'

    # Construct head meshes
    #     $ fg3 construct <FG_HEAD_PATH>/<head_model> <filename>.fg <filename>Head
    params = ['fg3', 'construct', os.path.join(FG_HEAD_PATH, head_model), filename+'.fg', filename+'Head']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False

    # Construct Mouth meshes
    #     $ fg3 construct <FG_MOUTH_PATH>/<mouth_model> <filename>.fg <filename>Mouth
    params = ['fg3', 'construct', os.path.join(FG_MOUTH_PATH, mouth_model), filename+'.fg', filename+'Mouth']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False

    # Construct Hair meshes
    #     $ fg3 construct <FG_HAIR_PATH>/<hair_model> <filename>.fg <filename>Hair
    params = ['fg3', 'construct', os.path.join(FG_HAIR_PATH, hair_model), filename+'.fg', filename+'Hair']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False

    # Copy hair color map
    #     $ cp <FG_HAIR_PATH>/<hair_model_color>.tga <filename>Hair.tga
    params = ['cp', os.path.join(FG_HAIR_PATH, hair_color+'.tga'), filename+'Hair.tga']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False

    return True


def render_model_to_png(filename: str) -> bool:
    
    '''Render face models to one PNG image without params

    By default the filenames of the head/face/mouth models follow the pattern
    as in construct_face_models().

    Parameters:
    filename (str):     filename of the .fg model

    Return:
        (boolean):      True if the PNG image is generated, False otherwise
    '''

    head_tri = filename + 'Head'
    head_bmp = filename + 'Head'
    mouth_tri = filename + 'Mouth'
    mouth_tga = filename + 'Mouth'
    hair_tri = filename + 'Hair'
    hair_tga = filename + 'Hair'

    return render_model_to_png_with_params(filename, head_tri, head_bmp, mouth_tri,
                                           mouth_tga, hair_tri, hair_tga)


def render_model_to_png_with_params(filename: str, head_tri: str,
                                    head_bmp: str, mouth_tri: str,
                                    mouth_tga: str, hair_tri: str,
                                    hair_tga: str) -> bool:

    '''Render face models to one PNG image with params

    Parameters:
    filename (str):     filename of the .fg file
    head_tri (str):     name of the head .tri file
    head_bmp (str):     name of the head .bmp file
    mouth_tri (str):    name of the mouth .tri file
    mouth_tga (str):    name of the mouth .tga file
    hair_tri (str):     name of the hair .tri file
    hair_tga (str):     name of the hair .tga file

    Return:
        (boolean):      True if the PNG image is generated, False otherwise
    '''

    params = ['fg3', 'render', filename+'Render',
              head_tri+'.tri', head_bmp+'.bmp',
              mouth_tri+'.tri', mouth_tga+'.tga',
              hair_tri+'.tri', hair_tga+'.tga']

    stdout, _ = _run_command(params)
    if stdout.startswith('ERROR'):
        print(stdout)
        return False

    return True

def change_pose(filename: str, roll: float, yaw: float, pitch: float):
    
    '''Change the pose of a given .xml renderer

    Parameters:
    filename (str):     filename of the .xml file
    roll (float):       roatation of roll, usually -1 to 1
    yaw (float):        rotation of yaw, usually -1 to 1
    pitch (float):      rotation of pitch, usually -1 to 1

    Return:
        (boolean):      True if the pose is changed, False otherwise
    '''

    pose_coord = [str(roll), str(yaw), str(pitch)]

    tree = ET.parse(filename+'.xml')
    for pose in tree.iter():
        if pose.tag == 'pose':
            break
    rotateToHcs = pose.find('rotateToHcs')
    idx = 0
    for item in rotateToHcs.iter():
        if item.tag == 'item':
            item.text = pose_coord[idx]
            idx += 1
    tree.write('a.xml')


def generate_one_face_img(filename: str, params: Dict[str, str]) -> bool:
    
    '''Generate a face image

    Parameters:
    filename (str): filename of the output face image

    Return:
        (boolean):      True if one face image is generated, False otherwise
    '''

    # parse params
    random = None if 'random' not in params else params['random']
    race = None if 'race' not in params else params['race']
    gender = None if 'gender' not in params else params['gender']

    init_face(filename, random, race, gender)


def _run_command(params: List[str]) -> str:

    '''Run command in terminal

    Parameters:
    params (list[str]): params of the command following the style as in subprocess module

    Return:
    stdout (str):       stdout from the terminal
    stderr (str):       stderr from the terminal
    '''

    cmd = sp.Popen(params,
                   stdout=sp.PIPE,
                   stderr=sp.STDOUT)
    stdout, stderr = cmd.communicate()

    stdout = str(stdout, 'utf-8').strip('\n') if stdout is not None else None
    stderr = str(stderr, 'utf-8').strip('\n') if stderr is not None else None

    return stdout, stderr


if __name__=='__main__':
    
    # print('Test generator:')
    # print('Init face model:')
    # print(init_face('test', None, None, None))
    # print('Get face params:')
    # print(get_face_params('test'))
    # print('Change face params:')
    # print(change_face_params('test', 'test1', 'age', '26'))
    # print('Construct face models:')
    # print(construct_face_models('test', None, None, None, None))
    # print('Render model to PNG:')
    # print(render_model_to_png('test'))
    change_pose('testRender', 1.0, 2.0, 3.0)

