# Copyright 2016-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Commands for adapters.
"""

from __future__ import absolute_import

import click

import zhmcclient
from .zhmccli import cli
from ._helper import print_properties, print_resources, abort_if_false, \
    options_to_properties, original_options, COMMAND_OPTIONS_METAVAR, \
    click_exception, add_options, LIST_OPTIONS
from ._cmd_cpc import find_cpc


def find_adapter(cmd_ctx, client, cpc_or_name, adapter_name):
    """
    Find an adapter by name and return its resource object.
    """
    if isinstance(cpc_or_name, zhmcclient.Cpc):
        cpc = cpc_or_name
    else:
        cpc = find_cpc(cmd_ctx, client, cpc_or_name)
    # The CPC must be in DPM mode. We don't check that because it would
    # cause a GET to the CPC resource that we otherwise don't need.
    try:
        adapter = cpc.adapters.find(name=adapter_name)
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)
    return adapter


@cli.group('adapter', options_metavar=COMMAND_OPTIONS_METAVAR)
def adapter_group():
    """
    Command group for managing adapters (DPM mode only).

    Physical adapters (e.g. OSA, FICON) are auto-discovered and cannot be
    created. Logical adapters (HiperSockets) can be created and deleted.

    The commands in this group work only on CPCs in DPM mode.

    In addition to the command-specific options shown in this help text, the
    general options (see 'zhmc --help') can also be specified right after the
    'zhmc' command name.
    """


@adapter_group.command('list', options_metavar=COMMAND_OPTIONS_METAVAR)
@click.argument('CPC', type=str, metavar='CPC')
@click.option('--type', is_flag=True, required=False, hidden=True)
@add_options(LIST_OPTIONS)
@click.pass_obj
def adapter_list(cmd_ctx, cpc, **options):
    """
    List the adapters in a CPC.

    In addition to the command-specific options shown in this help text, the
    general options (see 'zhmc --help') can also be specified right after the
    'zhmc' command name.
    """
    cmd_ctx.execute_cmd(lambda: cmd_adapter_list(cmd_ctx, cpc, options))


@adapter_group.command('show', options_metavar=COMMAND_OPTIONS_METAVAR)
@click.argument('CPC', type=str, metavar='CPC')
@click.argument('ADAPTER', type=str, metavar='ADAPTER')
@click.pass_obj
def adapter_show(cmd_ctx, cpc, adapter):
    """
    Show the details of an adapter.

    In addition to the command-specific options shown in this help text, the
    general options (see 'zhmc --help') can also be specified right after the
    'zhmc' command name.
    """
    cmd_ctx.execute_cmd(lambda: cmd_adapter_show(cmd_ctx, cpc, adapter))


@adapter_group.command('update', options_metavar=COMMAND_OPTIONS_METAVAR)
@click.argument('CPC', type=str, metavar='CPC')
@click.argument('ADAPTER', type=str, metavar='ADAPTER')
@click.option('--name', type=str, required=False,
              help='The new name of the adapter.')
@click.option('--description', type=str, required=False,
              help='The new description of the adapter.')
@click.option('--port-description', type=str, required=False,
              help='The new description of the single port of the adapter.')
@click.option('--mtu-size', type=click.Choice(['8', '16', '32', '56']),
              required=False,
              help='The new MTU size of the adapter in KiB. '
              '(HiperSockets only).')
@click.option('--allowed-capacity', type=int, required=False,
              help='The maximum number of HBAs per partition. '
              '(FCP only).')
@click.option('--chpid', type=str, required=False,
              help='Channel path ID (CHPID, 2 hex chars) used by the '
              'adapter\'s port. '
              '(OSA, FICON, HiperSockets only).')
@click.option('--crypto-number', type=int, required=False,
              help='Identifier of the crypto adapter in the range 0-15 '
              'Must be unique within the CPC. '
              '(Crypto only).')
@click.option('--crypto-tke/--no-crypto-tke', default=None, required=False,
              help='Permit TKE commands on the crypto adapter. '
              '(Crypto only).')
@click.pass_obj
def adapter_update(cmd_ctx, cpc, adapter, **options):
    """
    Update the properties of an adapter.

    Only the properties will be changed for which a corresponding option is
    specified, so the default for all options is not to change properties.

    The adapter may be a physical adapter (e.g. a discovered OSA card) or a
    logical adapter (e.g. HiperSockets).

    In addition to the command-specific options shown in this help text, the
    general options (see 'zhmc --help') can also be specified right after the
    'zhmc' command name.
    """
    cmd_ctx.execute_cmd(lambda: cmd_adapter_update(cmd_ctx, cpc, adapter,
                                                   options))


@adapter_group.command('create', options_metavar=COMMAND_OPTIONS_METAVAR)
@click.argument('CPC', type=str, metavar='CPC')
@click.option('--name', type=str, required=True,
              help='The name of the new adapter.')
@click.option('--description', type=str, required=False,
              help='The description of the new adapter. Default: empty')
@click.option('--port-description', type=str, required=False,
              help='The description of the (single) port of the new adapter. '
              'Default: empty')
@click.option('--mtu-size', type=click.Choice(['8', '16', '32', '56']),
              required=False,
              help='The MTU size of the new adapter in KiB. Default: 8')
@click.pass_obj
def adapter_create_hipersocket(cmd_ctx, cpc, **options):
    """
    Create a HiperSockets adapter in a CPC.

    In addition to the command-specific options shown in this help text, the
    general options (see 'zhmc --help') can also be specified right after the
    'zhmc' command name.

    Some more properties of the new HiperSockets adapter can be set via
    adapter update.
    """
    cmd_ctx.execute_cmd(
        lambda: cmd_adapter_create_hipersocket(cmd_ctx, cpc, options))


@adapter_group.command('delete', options_metavar=COMMAND_OPTIONS_METAVAR)
@click.argument('CPC', type=str, metavar='CPC')
@click.argument('ADAPTER', type=str, metavar='ADAPTER')
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              help='Skip prompt to confirm deletion of the adapter.',
              prompt='Are you sure you want to delete this adapter ?')
@click.pass_obj
def adapter_delete_hipersocket(cmd_ctx, cpc, adapter):
    """
    Delete a HiperSockets adapter.

    In addition to the command-specific options shown in this help text, the
    general options (see 'zhmc --help') can also be specified right after the
    'zhmc' command name.
    """
    cmd_ctx.execute_cmd(
        lambda: cmd_adapter_delete_hipersocket(cmd_ctx, cpc, adapter))


def cmd_adapter_list(cmd_ctx, cpc_name, options):
    # pylint: disable=missing-function-docstring

    client = zhmcclient.Client(cmd_ctx.session)
    cpc = find_cpc(cmd_ctx, client, cpc_name)

    try:
        adapters = cpc.adapters.list()
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)

    if options['type']:
        click.echo("The --type option is deprecated and type information "
                   "is now always shown.")

    show_list = [
        'name',
        'cpc',
    ]
    if not options['names_only']:
        show_list.extend([
            'adapter-id',
            'status',
            'adapter-family',
            'type',
            'detected-card-type',
            'crypto-type',
            'card-location',
        ])
    if options['uri']:
        show_list.extend([
            'object-uri',
        ])

    cpc_additions = {}
    for adapter in adapters:
        cpc_additions[adapter.uri] = cpc_name
    additions = {
        'cpc': cpc_additions,
    }

    try:
        print_resources(cmd_ctx, adapters, cmd_ctx.output_format, show_list,
                        additions, all=options['all'])
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)


def cmd_adapter_show(cmd_ctx, cpc_name, adapter_name):
    # pylint: disable=missing-function-docstring

    client = zhmcclient.Client(cmd_ctx.session)
    adapter = find_adapter(cmd_ctx, client, cpc_name, adapter_name)

    try:
        adapter.pull_full_properties()
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)

    print_properties(cmd_ctx, adapter.properties, cmd_ctx.output_format)


def cmd_adapter_update(cmd_ctx, cpc_name, adapter_name, options):
    # pylint: disable=missing-function-docstring

    client = zhmcclient.Client(cmd_ctx.session)
    adapter = find_adapter(cmd_ctx, client, cpc_name, adapter_name)

    name_map = {
        'mtu-size': 'maximum-transmission-unit-size',
        'chpid': 'channel-path-id',
        'crypto-tke': 'tke-commands-enabled',
    }
    org_options = original_options(options)
    properties = options_to_properties(org_options, name_map)

    if not properties:
        cmd_ctx.spinner.stop()
        click.echo("No properties specified for updating adapter '{a}'.".
                   format(a=adapter_name))
        return

    try:
        adapter.update_properties(properties)
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)

    cmd_ctx.spinner.stop()
    if 'name' in properties and properties['name'] != adapter_name:
        click.echo("Adapter '{a}' has been renamed to '{an}' and was updated.".
                   format(a=adapter_name, an=properties['name']))
    else:
        click.echo("Adapter '{a}' has been updated.".format(a=adapter_name))


def cmd_adapter_create_hipersocket(cmd_ctx, cpc_name, options):
    # pylint: disable=missing-function-docstring

    client = zhmcclient.Client(cmd_ctx.session)
    cpc = find_cpc(cmd_ctx, client, cpc_name)

    name_map = {
        'mtu-size': 'maximum-transmission-unit-size',
    }
    org_options = original_options(options)
    properties = options_to_properties(org_options, name_map)

    try:
        new_adapter = cpc.adapters.create_hipersocket(properties)
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)

    cmd_ctx.spinner.stop()
    click.echo("New HiperSockets adapter '{a}' has been created.".
               format(a=new_adapter.properties['name']))


def cmd_adapter_delete_hipersocket(cmd_ctx, cpc_name, adapter_name):
    # pylint: disable=missing-function-docstring

    client = zhmcclient.Client(cmd_ctx.session)
    adapter = find_adapter(cmd_ctx, client, cpc_name, adapter_name)

    try:
        adapter.delete()
    except zhmcclient.Error as exc:
        raise click_exception(exc, cmd_ctx.error_format)

    cmd_ctx.spinner.stop()
    click.echo("HiperSockets adapter '{a}' has been deleted.".
               format(a=adapter_name))
