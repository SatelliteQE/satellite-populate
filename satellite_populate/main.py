# coding: utf8
"""Point of entry for populate and validate used in scripts"""
import json
from collections import OrderedDict
from pprint import pformat

import fauxfactory
import import_string
import os
import yaml

from satellite_populate.constants import DEFAULT_CONFIG
from satellite_populate.utils import remove_keys, remove_nones


def setup_yaml():
    """Set YAML to use OrderedDict
    http://stackoverflow.com/a/8661021"""
    represent_dict_order = lambda self, data: self.represent_mapping(  # noqa
        'tag:yaml.org,2002:map', data.items()
    )
    yaml.add_representer(OrderedDict, represent_dict_order)


setup_yaml()


def load_data(datafile):
    """Loads YAML file as a dictionary"""
    if datafile.endswith(('.yml', '.yaml', 'json')):
        with open(datafile) as opened_file:
            data = yaml.load(opened_file)
            data['input_filename'] = datafile
            return data
    return yaml.load(datafile)


def get_populator(data, **kwargs):
    """Gets an instance of populator dynamically"""
    if not isinstance(data, dict):
        data = load_data(data)

    if not isinstance(data, dict):
        raise ValueError(
            "Data must be a valid filepath, dict, json or YAML string"
        )

    config = DEFAULT_CONFIG.copy()
    config.update(remove_nones(data.get('config', {})))
    config.update(remove_nones(kwargs))
    populator_name = config['populator']
    populator_module_name = config['populators'][populator_name]['module']
    populator_class = import_string(populator_module_name)
    populator = populator_class(data=data, config=config)
    return populator


def populate(data, **kwargs):
    """Loads and execute populator in populate mode"""
    kwargs = remove_nones(kwargs)
    populator = get_populator(data, **kwargs)
    populator.execute()
    populator.logger.info("%s finished!", populator.mode)

    if populator.mode == 'populate' and populator.config.get('enable_output'):
        save_rendered_data(
            populator,
            kwargs.get(
                'output'
            ) or "{0}.yaml".format(fauxfactory.gen_string('alpha'))
        )

    return populator


def default_context_wrapper(result):
    """Takes the result of populator and keeps only useful data
    e.g. in decorators context.registered_name, context.config.verbose and
    context.vars.admin_username will all be available.
    """
    context = result.registry
    context.config = result.config
    context.vars = result.vars
    return context


def save_rendered_data(result, filepath):
    """Save the result of rendering in a new file to be used for
    validation"""
    file_format = os.path.splitext(filepath)[-1]
    if file_format not in ('.json', '.yml', '.yaml', '.py'):
        raise ValueError("Invalid filename extension")

    data = OrderedDict({
        'input_filename': result.input_filename,
        'config': dict(result.config),
        'vars': dict(result.vars),
        'actions': result.rendered_actions
    })

    data['config']['mode'] = 'validate'
    data['config'] = remove_keys(data['config'], 'output')
    # should remove username, password, hostname ?

    data['config'] = remove_nones(data['config'])

    directory, filename = os.path.split(filepath)

    if not directory and data.get('input_filename'):
        directory = os.path.dirname(result.input_filename)

    if not filename.startswith('validation'):
        filename = "validation_{0}".format(filename)

    filepath = os.path.join(directory, filename)

    with open(filepath, 'w') as output:
        if file_format in ('.yml', '.yaml'):
            output.write(yaml.dump(data))
        elif file_format == '.json':
            output.write(json.dumps(data, indent=4))
        elif file_format == '.py':
            output.write("data = {0}".format(pformat(dict(data))))

    result.logger.debug("Validation data saved in %s", filepath)
