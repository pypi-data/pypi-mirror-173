# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models


class PaginationError(Exception):
    fmt = 'Pagination Exception: {message}'

    def __init__(self, **kwargs):
        msg = self.fmt.format(**kwargs)
        Exception.__init__(self, msg)
        self.kwargs = kwargs


def _get_next_token(response):
    if response and isinstance(response['body'], dict) and response['body']['NextToken']:
        return response['body']['NextToken']
    else:
        return None


class Paginator(TeaModel):
    def __init__(
            self,
            client: OpenApiClient = None,
            params: open_api_models.Params = None,
            request: open_api_models.OpenApiRequest = None,
            runtime: util_models.RuntimeOptions = None,
            model: TeaModel = None
    ):
        self.client = client
        self.params = params
        self.request = request
        self.runtime = runtime
        self.model = model
        self.next_token = None
        self.max_results = None
        self.first_request = True
        self.result_keys = []

    def validate(self):
        self.validate_required(self.params, 'params')
        if self.params:
            self.params.validate()
        self.validate_required(self.request, 'request')
        if self.request:
            self.request.validate()
        self.validate_required(self.runtime, 'runtime')
        if self.runtime:
            self.runtime.validate()
        self.validate_required(self.model, 'model')

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.params is not None:
            result['params'] = self.params.to_map()
        if self.request is not None:
            result['request'] = self.request.to_map()
        if self.runtime is not None:
            result['runtime'] = self.runtime.to_map()
        if self.model is not None:
            result['model'] = self.model
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('params') is not None:
            temp_model = open_api_models.Params()
            self.params = temp_model.from_map(m['params'])
        if m.get('request') is not None:
            temp_model = open_api_models.OpenApiRequest()
            self.request = temp_model.from_map(m['request'])
        if m.get('runtime') is not None:
            temp_model = util_models.RuntimeOptions()
            self.runtime = temp_model.from_map(m['runtime'])
        if m.get('model') is not None:
            self.model = m.get('model')
        return self

    def __iter__(self):
        if self.request.query['MaxResults']:
            self.max_results = self.request.query['MaxResults']
        if not self.max_results:
            raise StopIteration()
        if not self.next_token and not self.first_request:
            raise StopIteration()
        while True:
            if not self.first_request and self.next_token:
                if self.next_token in self.result_keys:
                    message = (
                        f"NextToken was received "
                        f"twice: {self.next_token}"
                    )
                    raise PaginationError(message=message)
                self.request.query['NextToken'] = self.next_token
            elif not self.first_request and not self.next_token:
                break
            response = self.client.call_api(self.params, self.request, self.runtime)
            self.result_keys.append(self.next_token)
            self.next_token = _get_next_token(response)
            parsed = self.model.from_map(response)
            self.first_request = False
            yield parsed
