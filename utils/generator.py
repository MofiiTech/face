import subprocess as sp

class FaceGenerator(face_id='tmp'):

    def __init__(self):
        
        params = ['fg3', 'create', 'random', 'any', 'any', face_id+'.fg']

        # Initialize a random face model
        #     $ fg3 random any any <face_id>.fg
        cmd = sp.Popen(params,
                       stdout=sp.PIPE,
                       stderr=sp.STDOUT)

    def get_age(

