import cro_validate.api.configuration_api as ConfigApi

def get_example_generator(definition, **kw):
	"""
	Get an instance of an example generator implementation via the configured factory.

	:returns: Example generator implementation.
	"""
	generator = ConfigApi.get_example_generator_factory().create(definition, **kw)
	return generator