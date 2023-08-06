"""Top-level package for AwsPClusterSlurmSpawner."""

__author__ = """ Jillian Rowe"""
__email__ = "jillian@dabbleofdevops.com"
__version__ = "0.1.0"

from aws_pcluster_slurm_spawner.aws_pcluster_slurm_spawner import (
    PClusterSlurmSpawner,
)

from . import _version

__version__ = _version.get_versions()["version"]
