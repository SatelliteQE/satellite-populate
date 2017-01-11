"""decorators for populate feature"""
from functools import wraps

from satellite_populate.main import populate, default_context_wrapper


def populate_with(data, context_name=None,
                  context_wrapper=default_context_wrapper, **extra_options):
    """To be used in test cases as a decorator

    Having a data_file like::

        actions:
          - model: Organization
            register: organization_1
            data:
              name: My Org

    Then you can use in decorators::

        @populate_with('file.yaml')
        def test_case_(self):
            'My Org exists in system test anything here'

    And getting the populated entities inside the test_case::

        @populate_with('file.yaml', context_name='context')
        def test_case_(self, context=None):
            assert context.entities.organization_1.name == 'My Org'

    You can also set a name to the context argument::

        @populate_with('file.yaml', context_name='my_context')
        def test_case_(self, my_context=None):
            assert my_context.organization_1.name == 'My Org'

    NOTE::

        That is important that ``context_name`` argument always be declared
        using either a default value ``my_context=None`` or handle in
        ``**kwargs`` Otherwise ``py.test`` may try to use this as a fixture
         placeholder.

    """

    def decorator(func):
        """Wrap test method"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """decorator wrapper"""

            result = populate(data, **extra_options)

            if context_name is not None:
                if context_wrapper:
                    context = context_wrapper(result)
                else:
                    context = result

                kwargs[context_name] = context

            return func(*args, **kwargs)

        return wrapper

    return decorator
