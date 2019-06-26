import re
import os
import subprocess as sp
from typing import List, Dict


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
        (boolean):      True if the model is initialized, otherwise False
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
        idx = [16, 14, 12, 10, 8, 6, 4, 2, 0]
        for i in idx:
            params.pop(i)
        return params


def change_face_params(param: str, value: str, filename: str ='tmp', newfilename: str ='tmp1') -> bool:

    '''Change the params of a given .fg face model

    Parameters:
    param (str):        the param name to be changed
    value (str):        the target value of the chosen param
    filename (str):     filename of the target face model, default 'tmp'
    newfilename (str):  filename of the new face model, default 'tmp1'

    Return:
        (boolean):      True if the param is changed, otherwise False
    '''
    
    params = ['fg3', 'controls', 'demographic', 'edit', filename+'.fg', param, value, newfilename+'.fg']

    cmd = sp.Popen(params,
                   stdout=sp.PIPE,
                   stderr=sp.STDOUT)
    stdout, _ = cmd.communicate()

    stdout = str(stdout, 'utf-8').strip('\n')
    if stdout.startswith('ERROR'):
        print(stdout)
        return False
    return True


def construct_face_models(filename: str ='tmp',
                  head_model: str ='HeadHires',
                  mouth_model: str ='Mouth',
                  hair_model: str='MidLengthStraight') -> bool:

    '''Construct face models: head, mouth, hair

    Parameters:
    filename (str):     filename of the selected face model
    head_model (str):   the head model in the directory <FG_HEAD_PATH>
    mouth_model (str):  the mouth model in the directory <FG_MOUTH_PATH>
    hair_model (str):   the hair model in the directory <FG_HAIR_PATH>

    Return:
        (boolean):      True if models are constructed, otherwise False
    '''

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

    return True


def generate_face_img(filename: str ='tmp', params: Dict[str, str]) -> bool:
    
    '''Generate a face image

    Parameters:
    -: -

    Return:
    -: -
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

    stdout = str(stdout, 'utf-8').strip('\n')
    stderr = str(stderr, 'utf-8').strip('\n')

    return stdout, stderr


if __name__=='__main__':
    
    # init_face('tmp')
    # get_face_params('tmp')
    change_face_params('age', '26')

