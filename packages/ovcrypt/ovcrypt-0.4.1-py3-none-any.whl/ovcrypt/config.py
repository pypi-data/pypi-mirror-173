import os
from ovcfg import Config


config_dirs = {
    "posix": [
        [os.path.join('/', 'var', 'lib'), []],
        [os.path.join(os.path.expanduser("~"), '.local'), ['share']]
    ],
    'nt': [
        [os.getenv('APPDATA'), []]
    ]
}


for config_dir in config_dirs[os.name]:
    if os.access(config_dir[0], os.W_OK):
        config_path = os.path.join(config_dir[0], *config_dir[1], 'ovcrypt')
        break
else:
    raise RuntimeError("Can't create ovcrypt config directory")


sc = {
    'rsa_server_public_key_file': os.path.join(config_path, 'keys', 'ov_public.pub'),
    'rsa_server_private_key_file': os.path.join(config_path, 'keys', 'ov_private.pem'),
    'key_size': 2048,
    'master_keys_url': 'http://example.com/master_keys'
}
cfg_class = Config(std_config=sc, file='ovcrypt.json', cfg_dir_name='overengine')
cfg = cfg_class.import_config()
