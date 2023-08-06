import os
import subprocess

from ... import paths


def preprocess(snakemake_args=[]):
    """Pre-processing step for the article build.

    Args:
        snakemake_args (list, optional): Additional options to pass to Snakemake.
    """
    snakefile = paths.showyourwork().workflow / "prep.smk"
    snakemake = f"SNAKEMAKE_OUTPUT_CACHE={paths.user().cache} SNAKEMAKE_RUN_TYPE='preprocess' snakemake -c1 --use-conda --conda-frontend conda --reason --cache"
    command = f"{snakemake} {' '.join(snakemake_args)} -s {snakefile}"
    result = subprocess.run(command, shell=True, check=False)
    if result.returncode > 0:
        os._exit(1)
