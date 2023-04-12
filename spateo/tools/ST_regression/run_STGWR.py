"""
Enables STGWR to be run using the "run" command rather than needing to navigate to and call the main file
(STGWR_mpi.py).
"""
import os
import sys

import click

# For now, add Spateo working directory to sys path so compiler doesn't look in the installed packages:
sys.path.insert(0, "/mnt/c/Users/danie/Desktop/Github/Github/spateo-release-main")
import spateo.tools.ST_regression as fast_stgwr


@click.group()
@click.version_option("0.3.2")
def main():
    pass


@main.command()
@click.option(
    "np",
    default=2,
    help="Number of processes to use. Note the max number of processes is " "determined by the number of CPUs.",
    required=True,
)
@click.option("adata_path")
@click.option("coords_key", default="spatial")
@click.option(
    "group_key",
    default="cell_type",
    help="Key to entry in .obs containing cell type "
    "or other category labels. Required if "
    "'mod_type' is 'niche' or 'slice'.",
)
@click.option(
    "csv_path",
    required=False,
    help="Can be used to provide a .csv file, containing gene expression data or any other kind of data. "
    "Assumes the first three columns contain x- and y-coordinates and then dependent variable "
    "values, in that order.",
)
@click.option("multiscale", default=False, is_flag=True)
@click.option(
    "mod_type",
    default="niche",
    help="If adata_path is provided, one of the STGWR models " "will be used. Options: 'niche', 'lr', 'slice'.",
)
@click.option("grn", default=False, is_flag=True)
@click.option("cci_dir", required=True)
@click.option("species", default="human")
@click.option(
    "output_path",
    default="./output/stgwr_results.csv",
    help="Path to output file. Make sure the parent " "directory is empty- any existing files will " "be deleted.",
)
@click.option("custom_lig_path", required=False)
@click.option("custom_rec_path", required=False)
@click.option(
    "custom_regulators_path",
    required=False,
    help="Only used for GRN models. This file contains a list "
    "of TFs (or other regulatory molecules)"
    "to constitute the independent variable block.",
)
@click.option("custom_targets_path", required=False)
@click.option(
    "target_expr_threshold",
    default=0.2,
    help="For automated selection, the threshold "
    "proportion of cells for which transcript "
    "needs to be expressed in to be selected as a target of interest. "
    "Not used if 'targets_path' is not None.",
)
@click.option("init_betas_path", required=False)
@click.option("normalize", default=False, is_flag=True)
@click.option("smooth", default=False, is_flag=True)
@click.option("log_transform", default=False, is_flag=True)
@click.option(
    "covariate_keys",
    required=False,
    multiple=True,
    help="Any number of keys to entry in .obs or "
    ".var_names of an "
    "AnnData object. Values here will be added to"
    "the model as covariates.",
)
@click.option("bw", required=False)
@click.option("minbw", required=False)
@click.option("maxbw", required=False)
@click.option(
    "bw_fixed",
    default=False,
    is_flag=True,
    help="If this argument is provided, the bandwidth will be "
    "interpreted as a distance during kernel operations. If not, it will be interpreted "
    "as the number of nearest neighbors.",
)
@click.option(
    "exclude_self",
    default=False,
    is_flag=True,
    help="When computing spatial weights, do not count the "
    "cell itself as a neighbor. Recommended to set to "
    "True for the CCI models because the independent "
    "variable array is also spatially-dependent.",
)
@click.option("kernel", default="bisquare")
@click.option("distr", default="gaussian")
@click.option("fit_intercept", default=False, is_flag=True)
@click.option("tolerance", default=1e-5)
@click.option("max_iter", default=1000)
@click.option(
    "patience",
    default=5,
    help="Number of iterations to wait before stopping if parameters have "
    "stabilized. Only used if `multiscale` is True.",
)
@click.option("alpha", required=False)
def run_STGWR(
    np,
    adata_path,
    coords_key,
    group_key,
    csv_path,
    multiscale,
    mod_type,
    grn,
    cci_dir,
    species,
    output_path,
    custom_lig_path,
    custom_rec_path,
    custom_regulators_path,
    custom_targets_path,
    target_expr_threshold,
    init_betas_path,
    normalize,
    smooth,
    log_transform,
    covariate_keys,
    bw,
    minbw,
    maxbw,
    bw_fixed,
    exclude_self,
    kernel,
    distr,
    fit_intercept,
    tolerance,
    max_iter,
    patience,
    alpha,
    chunks,
):
    """Command line shortcut to run any STGWR models.

    Args:
        n_processes: Number of processes to use. Note the max number of processes is determined by the number of CPUs.
        adata_path: Path to AnnData object containing gene expression data
        coords_key: Key to entry in .obs containing x- and y-coordinates
        group_key: Key to entry in .obs containing cell type or other category labels. Required if 'mod_type' is
            'niche' or 'slice'.
        csv_path: Can be used to provide a .csv file, containing gene expression data or any other kind of data.
            Assumes the first three columns contain x- and y-coordinates and then dependent variable values,
            in that order.
        multiscale: If True, the MGWR model will be used
        mod_type: If adata_path is provided, one of the STGWR models will be used. Options: 'niche', 'lr', 'slice'.
        grn: If True, the GRN model will be used
        cci_dir: Path to directory containing CCI files
        species: Species for which CCI files were generated. Options: 'human', 'mouse'.
        output_path: Path to output file
        custom_lig_path: Path to file containing a list of ligands to be used in the GRN model
        custom_rec_path: Path to file containing a list of receptors to be used in the GRN model
        custom_regulators_path: Only used for GRN models. This file contains a list of TFs (or other regulatory
            molecules) to constitute the independent variable block.
        custom_targets_path: Path to file containing a list of targets to be used in the GRN model
        target_expr_threshold: For automated selection, the threshold proportion of cells for which transcript needs
            to be expressed in to be selected as a target of interest.
        init_betas_path: Path to file containing initial values for beta coefficients
        normalize: If True, the data will be normalized
        smooth: If True, the data will be smoothed
        log_transform: If True, the data will be log-transformed
        covariate_keys: Any number of keys to entry in .obs or .var_names of an AnnData object. Values here will
            be added to the model as covariates.
        bw: Bandwidth to use for spatial weights
        minbw: Minimum bandwidth to use for spatial weights
        maxbw: Maximum bandwidth to use for spatial weights
        bw_fixed: If this argument is provided, the bandwidth will be interpreted as a distance during kernel
            operations. If not, it will be interpreted as the number of nearest neighbors.
        exclude_self: When computing spatial weights, do not count the cell itself as a neighbor. Recommended to
            set to True for the CCI models because the independent variable array is also spatially-dependent.
        kernel: Kernel to use for spatial weights. Options: 'bisquare', 'quadratic', 'gaussian', 'triangular',
            'uniform', 'exponential'.
        distr: Distribution to use for spatial weights. Options: 'gaussian', 'poisson', 'nb'.
        fit_intercept: If True, will include intercept in model
        tolerance: Tolerance for convergence of model
        max_iter: Maximum number of iterations for model
        patience: Number of iterations to wait before stopping if parameters have stabilized. Only used if
            `multiscale` is True.
        alpha: Alpha value to use for MGWR model
        chunks: Number of chunks for multiscale computation (default: 1). Increase the number if run out of memory
            but should keep it as low as possible.
        params_only:
    """

    mpi_path = os.path.dirname(fast_stgwr.__file__) + "/STGWR_mpi.py"

    command = (
        "mpiexec "
        + " -np "
        + str(np)
        + " python "
        + mpi_path
        + " -mod_type "
        + mod_type
        + " -species "
        + species
        + " -output_path "
        + output_path
        + " -target_expr_threshold "
        + str(target_expr_threshold)
        + " -coords_key "
        + coords_key
        + " -group_key "
        + group_key
        + " -kernel "
        + kernel
        + " -distr "
        + distr
        + " -tolerance "
        + str(tolerance)
        + " -max_iter "
        + str(max_iter)
        + " -patience "
        + str(patience)
    )

    if adata_path is not None:
        command += " -adata_path " + adata_path
    elif csv_path is not None:
        command += " -csv_path " + csv_path

    if multiscale:
        command += " -multiscale "
    if grn:
        command += " -grn "
    if cci_dir is not None:
        command += " -cci_dir " + cci_dir
    if custom_lig_path is not None:
        command += " -custom_lig_path " + custom_lig_path
    if custom_rec_path is not None:
        command += " -custom_rec_path " + custom_rec_path
    if custom_regulators_path is not None:
        command += " -custom_regulators_path " + custom_regulators_path
    if custom_targets_path is not None:
        command += " -custom_targets_path " + custom_targets_path
    if init_betas_path is not None:
        command += " -init_betas_path " + init_betas_path
    if normalize:
        command += " -normalize "
    if smooth:
        command += " -smooth "
    if log_transform:
        command += " -log_transform "
    if covariate_keys is not None:
        command += " -covariate_keys "
        for key in covariate_keys:
            command += key + " "
    if bw is not None:
        command += " -bw " + str(bw)
    if minbw is not None:
        command += " -minbw " + str(minbw)
    if maxbw is not None:
        command += " -maxbw " + str(maxbw)
    if bw_fixed:
        command += " -bw_fixed "
    if exclude_self:
        command += " -exclude_self "
    if fit_intercept:
        command += " -fit_intercept "
    if chunks is not None:
        command += " -chunks " + str(chunks)
    if alpha is not None:
        command += " -alpha " + str(alpha)

    os.system(command)
    pass


# ADD SOME DEFAULT OPTIONS LATER
