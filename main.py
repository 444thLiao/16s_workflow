import sys
from os.path import dirname,abspath

sys.path.insert(0, dirname(__file__))
import luigi
import click
from toolkit import run_cmd,get_dir_path



@click.group()
def cli():
    pass


@cli.command()
@click.argument('cmd', nargs=-1)
def run(cmd):
    luigi.run(cmdline_args=cmd)


@cli.command(help="analysis with test dataset, need to assign a output directory.")
@click.option("-o", "--odir", help="output directory for testing ...")
def testdata(odir):
    project_root_path = get_dir_path(__file__,1)
    run_cmd(
        f"python3 {project_root_path}/main.py run -- workflow --tab {project_root_path}/testset/seq_data/data_input.tsv --odir {odir} --analysis-type all --workers 4 --log-path {odir}/cmd_log.txt",
        dry_run=False)


class workflow(luigi.Task):
    tab = luigi.Parameter()
    odir = luigi.Parameter()
    analysis_type = luigi.Parameter(default="otu")
    dry_run = luigi.BoolParameter(default=False)
    log_path = luigi.Parameter(default=None)

    def requires(self):
        from tasks.unify_postanalysis import get_tree
        kwargs = dict(odir=self.odir,
                      tab=self.tab,
                      dry_run=self.dry_run,
                      log_path=self.log_path)
        return get_tree(analysis_type=self.analysis_type,
                        **kwargs)

    def run(self):
        pass


if __name__ == '__main__':
    # import pdb;pdb.set_trace()
    cli()
