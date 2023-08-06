from copy import deepcopy

from .constraints import (
    EnsureStr,
    EnsureConfigProcedureName,
    EnsureDatasetSiblingName,
    EnsureExistingDirectory,
    EnsureStrOrNoneWithEmptyIsNone,
)

# each item is a command that is allowed in the API
# the key is the command name in the Python API.
# the values are dicts with the following keys
# - exclude_parameters: set with parameter names to
#   exclude from the API

api = dict(
    clone=dict(
        name='&Clone a dataset',
        exclude_parameters=set((
            'git_clone_opts',
            'reckless',
            'description',
        )),
        parameter_display_names=dict(
            source='Clone from',
            path='Clone into',
            dataset='Register in superdataset',
        ),
        parameter_order=dict(
            source=0,
            path=1,
            dataset=2,
        ),
        parameter_constraints=dict(
            source=EnsureStr(min_len=1),
            path=EnsureExistingDirectory(allow_none=True),
        ),
    ),
    create=dict(
        name='C&reate a dataset',
        exclude_parameters=set((
            'initopts',
            'description',
            'fake_dates',
        )),
        parameter_display_names=dict(
            force='Force, if directory is not empty',
            path='Create at',
            dataset='Register in superdataset',
        ),
        parameter_order=dict(
            path=0,
            force=1,
            annex=2,
            dataset=3,
        ),
        parameter_constraints=dict(
            path=EnsureExistingDirectory(allow_none=True),
            cfg_proc=EnsureConfigProcedureName(allow_none=True),
        ),
    ),
    #create_sibling_gitlab=dict(
    #    name='Create a Git&Lab sibling',
    #    exclude_parameters=set((
    #        'dryrun',
    #        'path',
    #        'recursive',
    #    )),
    #),
    create_sibling_gin=dict(
        name='Create a GI&N sibling',
        exclude_parameters=set((
            'dryrun',
            'api',
            # bunch of complexity that can be ignored when not supporting
            # recursive sibling creation
            'path',
            'recursive',
            'dry_run',
            # GIN can take data, generally no strong need for this
            'publish_depends',
        )),
        parameter_display_names=dict(
            dataset='Create sibling for dataset at',
            reponame='New repository name on Gin',
            name='Sibling name',
            private='Make GIN repository private',
            existing='If the sibling exists already...',
            recursive='Create siblings for subdatasets',
            credential='Name of credential to be used',
            access_protocol='Get/push protocol',
            publish_depends='Add publication dependency to'
        ),
        parameter_order=dict(
            dataset=0,
            reponame=1,
            private=2,
            name=3,
            access_protocol=4,
            credential=5,
            existing=6,
        ),
        parameter_constraints=dict(
            name=EnsureStrOrNoneWithEmptyIsNone(),
        ),
    ),
    create_sibling_github=dict(
        name='Create a Git&Hub sibling',
        exclude_parameters=set((
            'dryrun',
            'github_login',
            'github_organization',
            'api',
            'path',
            'recursive',
        )),
        parameter_display_names=dict(
            dataset='Create sibling for dataset at',
            reponame='New repository name on Github',
            name='Sibling name',
            private='Make GitHub repo private',
            existing='If the sibling exists already...',
            recursive='Create siblings for subdatasets',
            credential='Name of credential to be used',
            access_protocol='Access protocol',
            publish_depends='Add publication dependency to'
        ),
        parameter_order=dict(
            dataset=0,
            reponame=1,
            private=2,
            name=3,
            access_protocol=4,
            existing=5,
            recursive=6,
            credential=7,
        ),
        parameter_constraints=dict(
            name=EnsureStrOrNoneWithEmptyIsNone(),
            publish_depends=EnsureDatasetSiblingName(allow_none=True),
        ),
    ),
    create_sibling_webdav=dict(
        name='Create a &WebDav sibling',
        exclude_parameters=set((
            # bunch of complexity that can be ignored when not supporting
            # recursive sibling creation
            'recursive',
            'path',
            'storage_name',
        )),
        parameter_display_names=dict(
            dataset='Create sibling for dataset at',
            url='WebDAV URL to create sibling at',
            name='Sibling name',
            mode='Usage mode for the sibling',
            credential='Name of credential to be used',
            existing='If the sibling exists already...',
        ),
        parameter_order=dict(
            dataset=0,
            url=1,
            name=2,
            mode=3,
            private=4,
            access_protocol=5,
            existing=6,
            credential=7,
        ),
        parameter_constraints=dict(
            name=EnsureStrOrNoneWithEmptyIsNone(),
            url=EnsureStr(min_len=len('http://e.c')),
        ),
    ),
    drop=dict(
        name='Dr&op content',
        exclude_parameters=set((
            'check',
            'if_dirty',
        )),
        parameter_display_names=dict(
            dataset='Drop from dataset at',
            what='What to drop',
            path='Limit to',
            recursive='Also drop (in) any subdatasets',
            reckless='Disable safeguards (reckless!)',
        ),
        parameter_order=dict(
            dataset=0,
            what=1,
            path=2,
            recursive=3,
            reckless=4,
        ),
    ),
    get=dict(
        name='&Get content',
        exclude_parameters=set((
            'description',
            'reckless',
            'source',
        )),
        parameter_default=dict(
            # we are no exposing this, hence we must provide a sane default,
            # which cannot be get everything always, but rather one level
            # at a time.
            recursion_limit=1,
        ),
        parameter_display_names=dict(
            dataset='Get content in dataset at',
            path='Limit to',
            recursive='Also get subdatasets',
            get_data='Get file content',
        ),
        parameter_order=dict(
            dataset=0,
            get_data=1,
            path=2,
            recursive=3,
        ),
    ),
    push=dict(
        name='&Push data/updates to a sibling',
        exclude_parameters=set((
            'since',
        )),
        parameter_constraints=dict(
            to=EnsureDatasetSiblingName(allow_none=True),
        ),
        parameter_display_names=dict(
            dataset='Push from dataset at',
            to='To dataset sibling',
            data='What to push',
            path='Limit to',
            force='Force operation',
        ),
        parameter_order=dict(
            dataset=0,
            to=1,
            data=2,
            path=3,
            recursive=4,
        ),
    ),
    save=dict(
        name='&Save the state in a dataset',
        exclude_parameters=set((
            'updated',
            'message_file',
        )),
        parameter_display_names=dict(
            dataset='Save changes in dataset at',
            message='Description of change',
            path='Limit to',
            recursive='Include changes in subdatasets',
            to_git='Do not put files in annex',
            version_tag='Tag for saved dataset state',
            amend='Amend last saved state',
        ),
        parameter_order=dict(
            dataset=0,
            message=1,
            path=2,
            recursive=3,
            to_git=4,
            version_tag=5,
            amend=6,
        ),
        parameter_constraints=dict(
            message=EnsureStrOrNoneWithEmptyIsNone(),
            version_tag=EnsureStrOrNoneWithEmptyIsNone(),
        ),
    ),
    update=dict(
        name='&Update from a sibling',
        exclude_parameters=set((
            'merge',
            'fetch_all',
            'how_subds',
            'follow',
            'reobtain_data',
        )),
        parameter_constraints=dict(
            sibling=EnsureDatasetSiblingName(allow_none=True),
        ),
        parameter_default=dict(
            # a merge "fetch", the actual default, would result in no
            # detectable changes within the GUI.
            how='merge',
        ),
    ),
)

dataset_api = {
    c: s for c, s in api.items()
    if c in (
        'clone', 'create',
        'create_sibling_gitlab', 'create_sibling_gin',
        'create_sibling_github', 'create_sibling_webdav',
        'drop', 'get', 'push', 'save', 'update'
    )
}
directory_api = {
    c: s for c, s in api.items() if c in ('clone', 'create')
}
directory_in_ds_api = {
    c: s for c, s in api.items()
    if c in ('clone', 'create', 'drop', 'get', 'push', 'save')
}
file_api = {}
file_in_ds_api = {
    c: s for c, s in api.items() if c in ('save')
}

annexed_file_api = {}
for c, s in api.items():
    if c not in ('drop', 'get', 'push', 'save'):
        continue
    s = deepcopy(s)
    # recursion underneath a file is not possible
    s['exclude_parameters'].add('recursive')
    # there can only ever be a single path
    s['parameter_nargs'] = dict(path=1)
    # path subselection does not make sense, but if we exclude it
    # the config dialog is practically empty. keep as some kind of
    # confirmation
    #s['exclude_parameters'].add('path')
    annexed_file_api[c] = s

# get of a single annexed files can be simpler
af_get = annexed_file_api['get']
# not getting data for an annexed file makes no sense
af_get['exclude_parameters'].add('get_data')


gooey_suite = dict(
    # may contain keyboard navigation hints
    title='&Simplified',
    description='Simplified access to the most essential operations',
    options=dict(
        disable_manual_path_input=True,
    ),
    apis=dict(
        dataset=dataset_api,
        directory=directory_api,
        directory_in_ds=directory_in_ds_api,
        file=file_api,
        file_in_ds=file_in_ds_api,
        annexed_file=annexed_file_api,
    ),
    # simplified API has no groups
    api_group_order={},
    exclude_parameters=set((
        'result_renderer',
        'return_type',
        'result_filter',
        'result_xfm',
        'on_failure',
        'jobs',
        'recursion_limit',
    )),
    parameter_display_names=dict(
        annex='Dataset with file annex',
        cfg_proc='Configuration procedure(s)',
        dataset='Dataset location',
    ),
)
