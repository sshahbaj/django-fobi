import logging
import re
from mimetypes import guess_type
import os
from string import Template

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from six import PY3

from ......base import IntegrationFormHandlerPlugin
from ......helpers import extract_file_path

from ... import UID as INTEGRATE_WITH_UID
from ...base import get_processed_serializer_data

from . import UID

__title__ = 'fobi.contrib.apps.drf_integration.' \
            'fobi_integration_form_handlers.mail.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'MailSenderHandlerPlugin',
)

LOGGER = logging.getLogger(__name__)


class MailSenderHandlerPlugin(IntegrationFormHandlerPlugin):
    """Mail sender handler form handler plugin.

    Can be used only once per form.
    """

    uid = UID
    name = _("Mail sender")
    integrate_with = INTEGRATE_WITH_UID

    def run(self,
            form_handler_plugin,
            form_entry,
            request,
            form_element_entries=None,
            **kwargs):
        """Run."""
        is_active = form_handler_plugin.plugin_data.get("is_active")
        form_field_name_to_email = form_handler_plugin.plugin_data.get("form_field_name_to_email")

        if form_field_name_to_email is None or form_field_name_to_email == "":
            return

        if not is_active:
            return

        base_url = form_handler_plugin.get_base_url(request)

        serializer = kwargs['serializer']

        # Clean up the values, leave our content fields and empty values.
        field_name_to_label_map, cleaned_data = get_processed_serializer_data(
            serializer,
            form_element_entries
        )

        rendered_data = form_handler_plugin.get_rendered_data(
            serializer.validated_data,
            field_name_to_label_map,
            base_url
        )

        files = self._prepare_files(request, serializer)

        subject_mapping = re.findall("\B\$\w+", form_handler_plugin.data.subject)
        body_mapping = re.findall("\B\$\w+", form_handler_plugin.data.body)
        subject_dict = {}
        body_dict = {}

        for i in subject_mapping:
            key = i[1:]
            if key == 'form_name':
                subject_dict['form_name'] = form_entry.name
            if key == 'first_name':
                subject_dict['first_name'] = request.user.first_name
            if key == 'last_name':
                subject_dict['last_name'] = request.user.last_name
            if key == 'email':
                subject_dict['email'] = request.user.email
        form_handler_plugin.data.subject = Template(form_handler_plugin.data.subject).substitute(**subject_dict)

        for j in body_mapping:
            key = j[1:]
            if key == 'form_name':
                body_dict['form_name'] = form_entry.name
            if key == 'first_name':
                body_dict['first_name'] = request.user.first_name
            if key == 'last_name':
                body_dict['last_name'] = request.user.last_name
            if key == 'email':
                body_dict['email'] = request.user.email
        form_handler_plugin.data.body = Template(form_handler_plugin.data.body).substitute(**body_dict)

        form_handler_plugin.send_email(rendered_data, cleaned_data, files)

    def _prepare_files(self, request, serializer):
        """Prepares the files for being attached to the mail message."""
        files = {}

        def process_path(file_path, imf):
            """Processes the file path and the file."""
            if file_path:
                file_path = file_path.replace(
                    settings.MEDIA_URL,
                    os.path.join(settings.MEDIA_ROOT, '')
                )
                mime_type = guess_type(imf.name)

                if PY3:
                    imf_chunks = b''.join([c for c in imf.chunks()])
                else:
                    imf_chunks = ''.join([c for c in imf.chunks()])

                files[field_name] = (
                    imf.name,
                    imf_chunks,
                    mime_type[0] if mime_type else ''
                )

        for field_name, imf in request.FILES.items():
            try:
                file_path = serializer.validated_data.get(field_name, '')
                process_path(file_path, imf)
            except Exception as err:
                file_path = extract_file_path(imf.name)
                process_path(file_path, imf)

        return files
