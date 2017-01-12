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

        @populate_with('file.yaml', context_name='my_context')
        def test_case_(self, my_context=None):
            assert my_context.organization_1.name == 'My Org'

    You can also set a customized context wrapper to the
    context_wrapper argument::

        def my_custom_context_wrapper(result):
            # create an object using result
            my_context = MyResultContext(result)
            return my_context

        @populate_with('file.yaml', context_name='my_context',
                       content_wrapper=my_custom_context_wrapper)
        def test_case_(self, my_context=None):
            # assert with some expression using my_context object returned
            # my_custom_context_wrapper
            assert some_expression

    NOTE::

        That is important that ``context_name`` argument always be declared
        using either a default value ``my_context=None`` or handle in
        ``**kwargs`` Otherwise ``py.test`` may try to use this as a fixture
         placeholder.

        if context_wrapper is set to None, my_context will be the pure
        unmodified result of populate function.

    """

    def decorator(func):
        """Wrap test method"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """decorator wrapper"""
            if not 'verbose' in extra_options:
                # set default verbose to -v so we get all messages in test log
                extra_options['verbose'] = 1
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
