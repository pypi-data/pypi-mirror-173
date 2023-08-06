import logging
import importlib.metadata

import pint


# Set the default logging level for the package
logging.basicConfig(level=logging.WARNING)
logging.captureWarnings(True)
pint.util.logger.setLevel(logging.ERROR)  # Mute Pint warnings


# Single-sourcing the package version
__version__ = importlib.metadata.version("cript")
__short_version__ = __version__.rpartition(".")[0]

__api_version__ = "0.6.0"

# Instantiate the Pint unit registry
# https://pint.readthedocs.io/en/stable/tutorial.html#using-pint-in-your-projects
# Note that this needs to be before the data model imports below
pint_ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)


from cript.data_model.paginator import Paginator
from cript.data_model import (  # noqa 402
    User,
    Group,
    Project,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    SoftwareConfiguration,
    Computation,
    Property,
    Identifier,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Equipment,
    Process,
    Experiment,
    Software,
    Parameter,
    Algorithm,
    ComputationalProcess,
    ComputationalForcefield,
)

DATA_MODEL_CLASSES = [
    User,
    Group,
    Project,
    Reference,
    Citation,
    Collection,
    File,
    Data,
    Condition,
    SoftwareConfiguration,
    Computation,
    Property,
    Identifier,
    Material,
    Inventory,
    Quantity,
    Ingredient,
    Equipment,
    Process,
    Experiment,
    Software,
    Parameter,
    Algorithm,
    ComputationalProcess,
    ComputationalForcefield,
]

DATA_MODEL_NAMES: list[str] = [node.node_name.lower() for node in DATA_MODEL_CLASSES]

from cript.api.rest import API  # noqa 401 402
from cript.api.local import APILocal
