import hashlib
import importlib.metadata
import importlib.resources
from contextlib import contextmanager
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional

from sphinx.application import Sphinx
from sphinx.util.fileutil import copy_asset_file

import furo_myst_nb_css_fixes

__version__ = importlib.metadata.version("furo_myst_nb_css_fixes")

CSS_RESOURCE = "furo-mystnb-fixes.css"


def _get_file_hash(path: Path) -> str:
    """Get the hash of a file. (Stolen from MyST-NB)"""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hashed_name(path: Path) -> Path:
    if not path.is_file():
        raise ValueError(f"Could not find given path to hash: {path}")
    return f"{path.name}.{_get_file_hash(path)}.{path.suffix}"


@contextmanager
def load_resource(resource) -> Path:
    if not importlib.resources.is_resource(furo_myst_nb_css_fixes, resource):
        raise ValueError(
            f"{resource} is an unknown resource! Something went wrong in the packaging!"
        )
    with importlib.resources.path(furo_myst_nb_css_fixes, resource) as resource_path:
        yield resource_path


def copy_resources(app: Sphinx, exception, resources: Optional[List[str]] = None):
    """
    Copy the local `resources` from the Python package to the
    Sphinx output directory `_static`.
    Note that these `resources` must be in the top-level of the package
    next to `__init__.py`.
    Should be wrapped with `partial` before connecting to `Sphinx` event.

    Args:
        app (Sphinx): Sphinx application
        exception: Do not run if exception is processed.
        resources (Optional[List[str]], optional): Optional list of resource names.
        If none are given, will return. Defaults to None.

    Raises:
        ValueError: If an unknown resource is given raise a `ValueError`.
    """
    if resources is None:
        return

    for resource in resources:
        with load_resource(resource) as resource_path:
            outdir = Path(app.outdir) / "_static"
            if exception is None:
                # needs to be copied under the hashed name...
                copy_asset_file(
                    str(resource_path), str(outdir / hashed_name(resource_path))
                )


def setup(app: Sphinx) -> Dict[str, Any]:
    copy_local_resources = partial(copy_resources, resources=[CSS_RESOURCE])

    app.connect("build-finished", copy_local_resources)
    # MyST-NB uses default priority for css:
    # https://github.com/executablebooks/MyST-NB/blob/master/myst_nb/sphinx_ext.py
    # Is already lower than furo, only furo extension is loaded later!
    with load_resource(CSS_RESOURCE) as resource_path:
        app.add_css_file(hashed_name(resource_path), priority=505)

    return {
        "version": __version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
