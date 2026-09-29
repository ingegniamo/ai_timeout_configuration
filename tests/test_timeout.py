# STeSI Consulting - Michele Di Croce
from unittest.mock import patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.ai.utils.llm_api_service import LLMApiService


@tagged('post_install', '-at_install')
class TestTimeout(TransactionCase):
    def _timeout_used(self, **kwargs):
        service = LLMApiService(env=self.env, provider='google')
        with patch('odoo.addons.ai.utils.llm_api_service.requests.request') as request:
            request.return_value.json.return_value = {}
            service._request('post', '/x', {}, {}, **kwargs)
        return request.call_args.kwargs['timeout']

    def test_default_without_parameter(self):
        self.assertEqual(self._timeout_used(), 120)

    def test_parameter(self):
        self.env['ir.config_parameter'].set_param('ai.request_timeout', '300')
        self.assertEqual(self._timeout_used(), 300)

    def test_invalid_parameter_falls_back(self):
        self.env['ir.config_parameter'].set_param('ai.request_timeout', 'abc')
        self.assertEqual(self._timeout_used(), 120)

    def test_explicit_timeout_wins(self):
        self.env['ir.config_parameter'].set_param('ai.request_timeout', '300')
        self.assertEqual(self._timeout_used(timeout=550), 550)
