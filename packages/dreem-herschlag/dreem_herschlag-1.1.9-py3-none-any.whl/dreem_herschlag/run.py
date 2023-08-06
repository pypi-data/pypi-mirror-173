#!/usr/bin/env python 

from email.policy import default
import click
from click_option_group import optgroup
import yaml
import os, sys

path = os.path.dirname('/'.join(os.path.abspath(__file__).split('/')[:-1]))
sys.path.append(path)

from dreem_herschlag.sanity_check import Sanity_check
from dreem_herschlag.run_dreem import Run_dreem

from dreem_herschlag.get_info import echo_attributes_samples, echo_attributes_library
from dreem_herschlag.templates import TemplateGenerator
from dreem_herschlag.generate_mh_only import generate_mh_only_folder
from dreem_herschlag.add_info import AddInfo
from dreem_herschlag.util import get_random_string
from dreem_herschlag import export

@click.command()
@optgroup.group("main arguments")
@optgroup.option("-c", "--config", type=click.Path(exists=True),
                 help="reference sequences in fasta format")
@optgroup.option("-r", "--rouskin", is_flag=True,
                 help="Use Rouskin lab templates")
@optgroup.option("--samples_info", is_flag=True, help="Print the mandatory and optional columns for samples.csv")
@optgroup.option("--library_info", is_flag=True, help="Print the mandatory and optional columns for library.csv")
@optgroup.option("--generate_templates", default=None, help="Path to generate templates for samples.csv (in_vivo and in_vitro) and library.csv")



def main(**args):
    """
    DREEM processes DMS next generation sequencing data to produce mutational
    profiles that relate to DMS modification rates written by Silvi Rouskin and the
    Rouskin lab (https://www.rouskinlab.com/)
    """
    run(args)

def read_config(args):
    with open(args['config'], 'r') as f:
        config = yaml.safe_load(f)
    assert config['samples'], "No samples found in config file"
    assert config['path_to_fastq_files'], "No path_to_fastq_files found in config file"
    assert config['path_to_dreem_output_files'], "No path_to_dreem_output_files found in config file"
    assert config['dreem_args'], "No dreem_args found in config file"
    assert config['verbose'] != None, "No verbose found in config file"
    assert config['fastq_zipped'] != None, "No fastq_zipped found in config file"
    for name, val in config['add_info_args'].items():
        config['use_'+name] = val if config['add_info'] else False      

    config['temp_folder'] = 'temp/'
    config['samples'] = [str(s) for s in config['samples']]
    for path in [k for k in config if k.startswith('path')]:
        config[path] = config[path]+'/' if config[path][-1]!= '/' else config[path]

    return config

def make_dirs():
    for repo in ['temp', 'output','log','input']:
        if not os.path.exists(repo):
            os.makedirs(repo)

def run(args):
    if args['samples_info']:
        echo_attributes_samples()
    if args['library_info']:
        echo_attributes_library()
    if args['generate_templates'] != None:
        TemplateGenerator(args['generate_templates']).run()
    if args['samples_info'] or args['library_info'] or args['generate_templates'] != None:
        exit()
    else:
        config = read_config(args)
        make_dirs()
        Sanity_check(config).run()
        if config['run_dreem']:
            print('Starting running DREEM')
            Run_dreem(config).run()
            generate_mh_only_folder(config)
        if config['add_info']:
            print('Starting add_info')
            AddInfo(config).run()
        if config['to_JSON']:
            export.to_json(config)            
        if config['to_CSV']:
            export.to_csv(config)
        print('Done!')

if __name__ == "__main__":
    sys.argv = ['run.py', '-c','config.yml']
    main()
