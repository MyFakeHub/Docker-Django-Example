import os

def get_docker_command(container_id):
    docker_command = '''
        docker run --rm --network=host --volumes-from web --gpus all \
        --name tf_{0} docker_tensorflow:latest \
        python tensorflow/app.py '''.format(container_id)
    return docker_command

def inspect_random_user():
    return os.system(get_docker_command(0) + '-a inspect_random_user')

def inspect_user(msisdn):
    return os.system(get_docker_command(0) + '-a inspect_user -m {0}'.format(msisdn))