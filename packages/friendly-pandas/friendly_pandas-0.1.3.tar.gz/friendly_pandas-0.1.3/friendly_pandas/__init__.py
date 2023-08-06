__version__ = "0.1.3"

import pathlib

import pandas
from friendly_traceback import (
    exclude_directory_from_traceback,
    config,
    add_other_module_names_synonyms,
)

# The following import will automatically add relevant parsers to
# those known by friendly_traceback
from . import specific
from . import generic

print(f"friendly_pandas version {__version__}")

# We want to focus on the code entered by the user.
# We remove anything that occurs inside pandas' library from the traceback
_pandas_init = pathlib.Path(pandas.__file__)
_pandas_dir = _pandas_init.parents[0]
exclude_directory_from_traceback(_pandas_dir)

# Disabling showing chained exceptions in normal "friendly" tracebacks
# as these likely come from code all inside pandas library.
# This will likely become the default in a future version.
config.session.include_chained_exception = False

add_other_module_names_synonyms(
    {"pd": "pandas", "np": "numpy", "plt": "matplotlib.pyplot"}
)
