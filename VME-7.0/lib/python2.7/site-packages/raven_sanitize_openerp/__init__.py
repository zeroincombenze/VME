# This file is part of openerp-sentry. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

"""
Based on raven.core.processors.SanitizePasswordsProcessor
"""

import re

from raven.processors import Processor
from raven.utils import varmap


class OpenerpPasswordsProcessor(Processor):
    """
    Asterisk out passwords from password fields in frames, http,
    and basic extra data.
    """
    MASK = '*' * 16
    RE_PASS = re.compile('( password=)\S+')

    def sanitize(self, key, value):
        if not key:  # key can be a NoneType
            return value

        key = key.lower()
        if 'password' in key or 'passwd' in key or 'secret' in key:
            # store mask as a fixed length for security
            return self.MASK

        if isinstance(value, basestring):
            return self.RE_PASS.sub('\g<1>%s' % self.MASK, value)

        return value

    def filter_stacktrace(self, data):
        if 'frames' not in data:
            return
        for frame in data['frames']:
            if 'vars' not in frame:
                continue
            self_obj = frame['vars'].get('self', '').split(' ')[0][1:]
            if (self_obj in ('netsvc.SimpleXMLRPCRequestHandler',
                             'netsvc.SecureXMLRPCRequestHandler',
                             'netsvc.LocalService')
                and 'params' in frame['vars']):
                if isinstance(frame['vars']['params'], tuple):
                    frame['vars']['params'] = list(frame['vars']['params'])
                frame['vars']['params'][2] = self.MASK
            else:
                frame['vars'] = varmap(self.sanitize, frame['vars'])

    def process(self, data, **kwargs):
        if 'sentry.interfaces.Stacktrace' in data:
            self.filter_stacktrace(data['sentry.interfaces.Stacktrace'])

        return data
