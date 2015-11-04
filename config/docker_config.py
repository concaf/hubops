from docker import Client
from config.logging_config import log_info,log_error

def docker_config():
    docker_protocol = 'http'
    docker_server = 'localhost'
    docker_port = 423

    docker_base_url = '{}://{}:{}/'.format(docker_protocol , docker_server , docker_port)

    def client_instance_verify(docker_base_url):
        test_client = Client(base_url=docker_base_url)

        try:
            test_client.version()['Version']
            log_info("Client initiated with version {}".format(test_client.version()['Version']))
            return docker_base_url

        except:
            log_error("Connection error.")
            return False

        del test_client

    return client_instance_verify(docker_base_url)