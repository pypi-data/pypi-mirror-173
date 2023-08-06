import cro_validate.api.configuration_api as ConfigApi


def create_input_error(source, message, internal_message=None, exception=None, **kw):
	"""
	Create instance of input error. The factory implementation can be configured via :ref:`cro_validate.api.configuration_api.set_exception_factory`. See the :doc:`Error Handling Guide </error_guide>`.

	:returns: Input error instance.
	"""
	return ConfigApi.get_exception_factory().create_input_error(source, message, internal_message, exception, **kw)


def create_internal_error(source, message, exception=None, **kw):
	"""
	Create instance of internal error. The factory implementation can be configured via :ref:`cro_validate.api.configuration_api.set_exception_factory`. See the :doc:`Error Handling Guide </error_guide>`.

	:returns: Internal error instance.
	"""
	return ConfigApi.get_exception_factory().create_internal_error(source, message, exception, **kw)