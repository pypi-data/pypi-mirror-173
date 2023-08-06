import os

def generate_mh_only_folder(config):
    if not os.path.exists(config['path_to_dreem_output_files']):
        os.mkdir(config['path_to_dreem_output_files'])
    for s in config['samples']:
        os.system(f"cp output/{s}/BitVector_Files/mh.p {config['path_to_dreem_output_files']}{s}.p")
        print(f"mh_only/{s}.p written")