import os
import subprocess

from ... import paths


def tarball(options=""):
    """Build the article tarball.

    Args:
        options (str, optional): Additional options to pass to Snakemake.
    """
    snakefile = paths.showyourwork().workflow / "build.smk"
    snakemake = f"SNAKEMAKE_OUTPUT_CACHE={paths.user().cache} SNAKEMAKE_RUN_TYPE='tarball' snakemake -c1 --use-conda --conda-frontend conda --reason --cache"
    command = f"{snakemake} {options} -s {snakefile} syw__arxiv_entrypoint"
    result = subprocess.run(command, shell=True, check=False)
    if result.returncode > 0:
        os._exit(1)
