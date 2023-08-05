# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_paginator import models as paginator_models


class Client:

    @staticmethod
    def paginate(
            self,
            client: OpenApiClient,
            params: open_api_models.Params,
            request: open_api_models.OpenApiRequest,
            runtime: util_models.RuntimeOptions,
            model: TeaModel,
    ) -> paginator_models.Paginator:
        """
        Gets a paginator
        @return: the paginator Paginator
        """
        return paginator_models.Paginator(
            client=client,
            params=params,
            request=request,
            runtime=runtime,
            model=model
        )
