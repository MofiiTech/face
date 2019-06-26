import re
import subprocess as sp


def generate_face(filename: str ='tmp', random: str ='random', race: str ='any', gender: str ='any'):
    
    '''Generate a face image with parameters
    
    Parameters:
    filename (str):     filename for local tmp files, default 'tmp'
    random (str):       face domain, default 'random'
                            [random, average]
    race (str):         race param of the face, default 'any'
                            [african | european | eastAsian | southAsian | any]
    gender (str):       gender param of the face, default 'any'
                            [male | female | any]

    Return:
    -: -
    '''

    params = ['fg3', 'create', random, race, gender, filename+'.fg']

    # Generate a random face:
    #     $ fg3 random any any <filename>.fg
    cmd = sp.Popen(params,
                   stdout=sp.PIPE,
                   stderr=sp.STDOUT)


def get_face_params(filename: str ='tmp'):

    '''Get the params of a given .fg face model

    Parameters:
    filename (str): filename of the target face model, default='tmp'

    Return:
    params (list[str]): a list of face params
                            [<age>, <gender>, <caricature shape>, <caricature color>,
                            <asymmetry>, <african>, <east asian>, <south asian>,
                            <european>]
    '''
    
    params = ['fg3', 'controls', 'demographic', 'edit', filename+'.fg']

    cmd = sp.Popen(params,
                   stdout=sp.PIPE,
                   stderr=sp.STDOUT)
    stdout, _ = cmd.communicate()

    stdout = str(stdout, 'utf-8').strip('\n')
    if stdout.startswith('ERROR'):
        print(stdout)
        return None
    else:
        params = re.split('\s', stdout)
        idx = [16, 14, 12, 10, 8, 6, 4, 2, 0]
        for i in idx:
            params.pop(i)
        return params


def change_face_params(param: str, value: str, filename: str ='tmp', newfilename: str ='tmp1'):

    '''Change the params of a given .fg face model

    Parameters:
    param (str):        the param name to be changed
    value (str):        the target value of the chosen param
    filename (str):     filename of the target face model, default 'tmp'
    newfilename (str):  filename of the new face model, default 'tmp1'

    Return:
        (boolean):      True if the param is changed, False if failed
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


if __name__=='__main__':
    
    # generate_face()
    # get_face_params('tmp')
    change_face_params('age', '26')

