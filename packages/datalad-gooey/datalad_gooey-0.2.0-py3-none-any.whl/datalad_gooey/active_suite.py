from types import MappingProxyType
from datalad import cfg

spec = None
# names of parameters to exclude for any command
# exclude_parameters = set()

# mapping of parameter names to display names
# to be applied across all commands
# parameter_display_names = {}

# mapping of group name/title to sort index
# api_group_order = {}

#
# API specifications
#
# commands that operate on datasets
dataset_api = None
# commands that operate on any directory
directory_api = None
# commands that operate on directories in datasets
directory_in_ds_api = None
# commands that operate on any file
file_api = None
# commands that operate on any file in a dataset
file_in_ds_api = None
# command that operate on annex'ed files
annexed_file_api = None
# commands that have no specific target type, or another than
# dataset, dir, file etc from above
other_api = None


active_suite = cfg.obtain('datalad.gooey.active-suite')
epname = 'datalad.gooey.suites'

from datalad.support.entrypoints import iter_entrypoints
for sname, _, sload in iter_entrypoints(epname, load=False):
    if sname != active_suite:
        continue

    # deposit the spec in read-only form
    spec = MappingProxyType(sload())

    # deploy convenience importable symbols
    for apiname, api in spec.get('apis', {}).items():
        globals()[f"{apiname}_api"] = api

if spec is None:
    raise RuntimeError(
        f'No Gooey suite {active_suite!r}! Have: '
        f'{[n for n, _, _ in iter_entrypoints(epname, load=False)]}'
        ' Imploding...')

    api = dict()
    for a in active_suite.get('apis', {}).values():
        if a:
            api.update(a)
