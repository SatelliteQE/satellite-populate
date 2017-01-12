# coding: utf-8
"""
Tests for satellite_populate module and commands
"""
import pytest
from unittest2 import TestCase
from satellite_populate import populate_with


data_in_dict = {
    'actions': [
        {
            'action': 'register',
            'data': {
                'project': 'Satellite'
            }
        }
        # CRUD ACTIONS DEMANDS MOCK OF API
        # {
        #     'model': 'Organization',
        #     'register': 'organization_1',
        #     'data': {
        #         'name': 'My Organization 1',
        #         'label': 'my_organization_1'
        #     }
        # },
        # {
        #     'model': 'Organization',
        #     'register': 'organization_2',
        #     'data': {
        #         'name': 'My Organization 2',
        #         'label': 'my_organization_2'
        #     }
        # }
    ]
}

data_in_string = """
actions:
  - action: register
    data:
      name: Michael
      lastname: Scott
      company: Dunder Mifflin
      fake_repo:
        from_object: nailgun.entities._FAKE_YUM_REPO
      random:
        from_factory:
          alpha: 10
      should_not_exist: "This will be unregistered below"

  - action: assertion
    operation: eq
    data:
      - Hello
      - Hello
    register: hello_equals_hello

  - action: unregister
    data:
      - should_not_exist
"""


class CustomizedResultContext(object):
    """a simple customized result context wrapper object"""

    def __init__(self, result):
        self.__result = result

    @classmethod
    def wrapper(cls, result):
        return cls(result)

    @property
    def result(self):
        return self.__result

    @property
    def registry(self):
        return self.result.registry

    @property
    def vars(self):
        return self.result.vars

    @property
    def config(self):
        return self.result.config

    def __getattr__(self, name):
        return getattr(self.result.registry, name)


@populate_with(data_in_dict, context_name='context', verbose=1)
def test_data_in_dict(context=None):
    """a test with populated data"""
    assert context.project == "Satellite"


@populate_with(data_in_dict, context_name='context',
               context_wrapper=CustomizedResultContext.wrapper,
               verbose=0)
def test_data_in_dict_and_customized_wrapper(context=None):
    """a test with populated data and customized wrapper"""
    assert isinstance(context, CustomizedResultContext)
    assert context.project == context.registry.project
    assert context.project == "Satellite"


@populate_with(data_in_string, context_name='context', verbose=1)
def test_data_in_string(**kwargs):
    """a test with populated data"""
    context = kwargs['context']
    assert context.name == 'Michael'
    assert context.lastname == 'Scott'
    assert context.company == 'Dunder Mifflin'
    fake_repo = 'http://inecas.fedorapeople.org/fakerepos/zoo3/'
    assert context.fake_repo == fake_repo
    assert len(context.random) == 10
    assert context.hello_equals_hello is True
    with pytest.raises(KeyError):
        assert context.should_not_exist == "This will be unregistered below"


class MyTestCase(TestCase):
    """
    THis test populates data in setUp and also in individual tests
    """
    @populate_with(data_in_string, context_name='context')
    def setUp(self, context=None):
        self.context = context

    def test_with_setup_data(self):
        context = self.context
        self.assertEqual(context.name, 'Michael')
        self.assertEqual(context.lastname, 'Scott')
        self.assertEqual(context.company, 'Dunder Mifflin')
        fake_repo = 'http://inecas.fedorapeople.org/fakerepos/zoo3/'
        self.assertEqual(context.fake_repo, fake_repo)
        self.assertEqual(len(context.random), 10)
        self.assertTrue(context.hello_equals_hello)

        with self.assertRaises(KeyError):
            self.assertEqual(context.should_not_exist,
                             "This will be unregistered below")

    @populate_with(data_in_dict, context_name='test_context')
    def test_with_isolated_data(self, test_context=None):
        self.assertEqual(
            test_context.project, "Satellite"
        )
