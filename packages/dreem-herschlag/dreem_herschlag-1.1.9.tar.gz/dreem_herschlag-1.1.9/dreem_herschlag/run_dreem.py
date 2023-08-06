from dreem_herschlag.util import run_command
from dreem_herschlag.sanity_check import Sanity_check


class Run_dreem(object):
    def __init__(self, config) -> None:
        self.samples = config['samples']
        self.path_to_fastq_files = config['path_to_fastq_files']
        self.dreem_args = config['dreem_args']
        self.verbose = config['verbose']
        self.fastq_zipped = config['fastq_zipped']
        self.fasta_file = Sanity_check(config).find_fasta()
        self.config = config
        self.suffix_cmd = self.dreem_args.pop('suffix_cmd')


    def run(self):
        if self.verbose: print(f"Running DREEM")
        for s in self.samples:
            cmd = 'dreem'
            for fast_arg, fast_file in zip(['-fq1','-fq2'],[x + '.gz' if self.fastq_zipped else x for x in ['_R1_001.fastq', '_R2_001.fastq']]):
                cmd += ' '+fast_arg+' '+self.path_to_fastq_files+s+fast_file

            cmd += ' -fa '+self.fasta_file
            cmd += ' --sample '+s

            for key, val in self.dreem_args.items():
                if key == 'RNAstructure' and val:
                    cmd += ' --RNAstructure_path '+self.config['path_to_RNAstructure']
                if (not (type(val) == bool)) or val:
                    cmd += ' --'+ key + ' '+ (str(val) if type(val) != bool else '')
            cmd += ' '+self.suffix_cmd

            if self.verbose: print(cmd)
            [print(out) for out in run_command(cmd)] if self.verbose else run_command(cmd)
        if self.verbose: print('DREEM done\n')