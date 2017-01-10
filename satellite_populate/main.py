# coding: utf8
"""Point of entry for populate and validate used in scripts"""
import json
from collections import OrderedDict

import import_string
import os
import yaml
from satellite_populate.constants import DEFAULT_CONFIG


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
        with open(datafile) as datafile:
            return yaml.load(datafile)
    return yaml.load(datafile)


def get_populator(data, verbose):
    """Gets an instance of populator dynamically"""
    if not isinstance(data, dict):
        data = load_data(data)

    config = DEFAULT_CONFIG.copy()
    config.update(data.get('config', {}))
    verbose = verbose or config.get('verbose')

    populator_name = config['populator']
    populator_module_name = config['populators'][populator_name]['module']
    populator_class = import_string(populator_module_name)
    populator = populator_class(data=data, verbose=verbose, config=config)
    return populator


def populate(data, **extra_options):
    """Loads and execute populator in populate mode"""
    verbose = extra_options.get('verbose')
    populator = get_populator(data, verbose)
    populator.execute(mode='populate')
    populator.logger.info("Populator finished!")
    if extra_options.get('output'):
        save_rendered_data(populator, extra_options['output'])
    return populator


def validate(data, **extra_options):
    """Loads and execute populator in validate mode"""
    verbose = extra_options.get('verbose')
    populator = get_populator(data, verbose)
    populator.execute(mode='validate')
    populator.logger.info("Validator finished!")
    if extra_options.get('output'):
        save_rendered_data(populator, extra_options['output'])
    return populator


def wrap_context(result):
    """Takes the result of populator and keeps only useful data
    e.g. in decorators context.registered_name, context.config.verbose and
    context.vars.admin_username will all be available.
    """
    context = result.registry
    context.config = result.config
    context.vars = result.vars
    return context


def save_rendered_data(result, filename):
    """Save the result of rendering in a new file to be used for
    validation"""
    file_format = filename.rsplit('.')[-1]
    if file_format not in ('json', 'yml', 'yaml', 'py'):
        raise ValueError("Invalid filename extension")

    data = OrderedDict({
        'config': dict(result.config),
        'vars': dict(result.vars),
        'actions': result.rendered_actions
    })

    if not filename.startswith('validation_'):
        filename = "validation_{0}".format(filename)

    with open(filename, 'w') as output:
        if file_format in ('yml', 'yaml'):
            output.write(yaml.dump(data))
        elif file_format == 'json':
            output.write(json.dump(data))
        elif file_format == 'py':
            output.write(str(data))

    result.logger.debug("Validation data saved in %s", filename)
