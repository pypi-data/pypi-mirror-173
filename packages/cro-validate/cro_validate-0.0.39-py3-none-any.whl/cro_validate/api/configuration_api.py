from cro_validate.classes.configuration_classes import Config

def get_exception_factory():
	"""
	Return the exception factory used for generating exceptions. See the Error Handling Guide for more info.

	:returns: Return the configured exception facotry.
	"""
	return Config.exception_factory


def set_exception_factory(f):
	"""
	Set the configuration factory to use to generate exceptions. See the :doc:`Error Handling Guide </error_guide>` for more info.
	:returns: None
	"""
	Config.exception_factory = f


def get_definition_name_resolver():
	"""
	Return the configured definition name resolver instance. See the Naming Guide for more info.

	:returns: Return the configured definition name resolver instance.
	"""
	return Config.definition_name_resolver


def set_definition_name_resolver(r):
	"""
	Set the name resolver to use. See the Naming Guide for more info.

	:param r: Resolver implementation. See :ref:`cro_validate.classes.name_resolver_classes.DefaultNameResolver` for an example implementation.
 	:returns: None
	"""
	Config.definition_name_resolver = r


def get_parameter_name_resolver():
	"""
	Set the name resolver to use. See the Naming Guide for more info.

	:returns: Name resolver implementation.
	"""
	return Config.parameter_name_resolver


def set_parameter_name_resolver(r):
	"""
	Set the name resolver to use. See the Naming Guide for more info.

	:param r: Name resolver implementation.
	:returns: None
	"""
	Config.parameter_name_resolver = r


def get_example_generator_factory():
	"""
	Get example generator factory. See :doc:`Example Generation Guide </example_generation_guide.rst>`

	:returns: Example generator factory implementation.
	"""
	return Config.example_generator_factory


def set_example_generator_factory(f):
	"""
	Set the example generator factory to use. See the :doc:`Example Generation </example_generation_guide>` for more info.

	:param r: Name resolver implementation.
	:returns: None
	"""
	Config.example_generator_factory = f


def set_definition_name_strategy(s):
	"""
	Set the definition name strategy. See the :doc:`Naming Guide </naming_guide>`

	:param s: Naming strategy implementation.
	:returns: None
	"""
	Config.definition_name_strategy = s


def get_definition_name_strategy():
	"""
	Get the configured definition naming strategy.

	:returns: Definition naming strategy implementation.
	"""
	return Config.definition_name_strategy


def set_instantiate_value_provider(p):
	"""
	Sets the instantiation provider implementation. See :ref:`cro_validate.classes.definition_classes.InstantiateValueProvider`.

	:param p: Instantiation provider implementation.
	"""
	Config.instantiate_value_provider = p


def get_instantiate_value_provider():
	"""
	Get the instantiation provider implementation.

	:returns: Instantiation provider implemenation.
	"""
	return Config.instantiate_value_provider