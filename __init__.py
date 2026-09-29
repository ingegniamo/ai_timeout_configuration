# STeSI Consulting - Michele Di Croce
from odoo.addons.ai.utils.llm_api_service import LLMApiService

DEFAULT_TIMEOUT = 120

_request_base = LLMApiService._request


def _request(self, *args, **kwargs):
    # calls that pass their own timeout (audio transcription) keep it
    if 'timeout' not in kwargs:
        param = self.env['ir.config_parameter'].sudo().get_param('ai.request_timeout')
        try:
            kwargs['timeout'] = int(param) if param else DEFAULT_TIMEOUT
        except ValueError:
            kwargs['timeout'] = DEFAULT_TIMEOUT
    return _request_base(self, *args, **kwargs)


LLMApiService._request = _request
