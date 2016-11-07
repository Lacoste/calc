from functools import wraps
from django.conf.urls import url
from django.contrib import messages
from django.shortcuts import render
from django.template.defaultfilters import pluralize
from django.template.loader import render_to_string


def add_generic_form_error(request, form):
    messages.add_message(
        request, messages.ERROR,
        'Oops! Please correct the following error.'
            .format(pluralize(form.errors))
    )


class Steps:
    '''
    The `Steps` class makes it easier to consolidate the logic of
    multi-step workflows.

    The `Steps` constructor takes a format string representing what
    the template path for each step looks like:

        >>> steps = Steps('data_capture/tests/my_step_{}.html')

    The `@step` view decorator can be used to "register" steps in the
    workflow.  Each step's function name is expected to end with
    a number, and the steps are expected to be defined in
    ascending order, e.g.:

        >>> @steps.step
        ... def step_1(request, step): pass

        >>> @steps.step
        ... def step_2(request, step): pass

    (What's that extra `step` argument?  We'll get to that in a moment!)

    Breaking this ordering, e.g. by skipping numbers, is not allowed:

        >>> @steps.step
        ... def step_5(request, step): pass
        Traceback (most recent call last):
        ...
        ValueError: Expected "step_5" to end with the number 3

    At this point, our example workflow has two steps:

        >>> steps.num_steps
        2

    URL patterns for our steps are automatically defined, too, and can
    be included via Django's standard `include()` function. The names
    of each view will be identical to their view function's name:

        >>> steps.urls
        [<RegexURLPattern step_1 ^1$>, <RegexURLPattern step_2 ^2$>]

    Now, what's that `step` argument passed into each view function?

    It's a `StepRenderer` instance bound to the particular step that the
    view represents, and it provides some tools that make it easy to
    render steps.

    `StepRenderer` instances can also be retrieved manually if needed:

        >>> step1 = steps.get_step_renderer(1)

    A `StepRenderer` instance can be used to easily access
    commonly-used view logic, e.g.:

        >>> step1.number
        1

        >>> step1.steps.num_steps
        2

        >>> step1.description
        'step 1 of 2'

    Tools for templates and their contexts are also available.

    The `context()` function builds a context dictionary that always
    contains a `step` key referring to the `StepRenderer` instance for
    that step:

        >>> ctx = step1.context({'foo': 'bar'})
        >>> ctx['foo']
        'bar'
        >>> ctx['step']
        <StepRenderer for step 1 of 2>

    The `template_name` property always refers to the template for the step:

        >>> step1.template_name
        'data_capture/tests/my_step_1.html'

    And `render`/`render_to_string` ties everything together:

        >>> step1.render_to_string({'foo': 'bar'})
        'Hello from step 1 of 2! foo is bar.'
    '''

    def __init__(self, template_format, extra_ctx_vars=None):
        self.extra_ctx_vars = extra_ctx_vars or {}
        self.template_format = template_format
        self._views = []

    def step(self, func):
        step_number = self.num_steps + 1

        if not func.__name__.endswith(str(step_number)):
            raise ValueError('Expected "{}" to end with the number {}'.format(
                func.__name__,
                step_number
            ))

        @wraps(func)
        def wrapper(*args, **kwargs):
            kwargs['step'] = self.get_step_renderer(step_number)
            return func(*args, **kwargs)

        self._views.append(wrapper)
        return wrapper

    def get_step_renderer(self, step_number):
        return StepRenderer(self, step_number)

    @property
    def urls(self):
        urlpatterns = []

        for i in range(self.num_steps):
            view = self._views[i]
            regex = r'^' + str(i + 1) + r'$'
            urlpatterns.append(url(regex, view, name=view.__name__))

        return urlpatterns

    @property
    def num_steps(self):
        return len(self._views)


class StepRenderer:
    def __init__(self, steps, step_number):
        self.steps = steps
        self.number = step_number

    def context(self, context=None):
        final_ctx = {'step': self}
        final_ctx.update(self.steps.extra_ctx_vars)
        if context:
            final_ctx.update(context)
        return final_ctx

    @property
    def template_name(self):
        return self.steps.template_format.format(self.number)

    def render(self, request, context=None):
        return render(request, self.template_name,
                      self.context(context))

    def render_to_string(self, context=None):
        return render_to_string(self.template_name, self.context(context))

    @property
    def description(self):
        return "step {} of {}".format(
            self.number,
            self.steps.num_steps
        )

    def __repr__(self):
        return '<{} for {}>'.format(
            self.__class__.__name__,
            self.description
        )