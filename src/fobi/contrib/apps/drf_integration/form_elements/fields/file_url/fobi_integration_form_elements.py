from .......base import integration_form_element_plugin_registry
from .base import FileURLInputPlugin

__title__ = 'fobi.contrib.apps.drf_integration.form_elements.fields.' \
            'file_url.fobi_integration_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FileURLInputPlugin',)


integration_form_element_plugin_registry.register(FileURLInputPlugin)
