#!/usr/bin/env python
"""
exceptions.py
"""

import logging

from django.http import Http404
from django.utils.translation import gettext_lazy as _
from rest_framework import status, exceptions
from rest_framework.exceptions import (
    APIException,
    ValidationError,
    AuthenticationFailed,
    PermissionDenied,
    NotAuthenticated,
)
from rest_framework.views import exception_handler, set_rollback

from drfcommon.choices import ComCodeChoice
from drfcommon.response import done

logger = logging.getLogger('debug')


class MyValidationError(ValidationError):
    """
    MyValidation Error
    """
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, detail=None, code=None):
        logger.error('ValidationError detail:{} code:{}'.format(detail, code))
        if code:
            self.status_code = code
        super(MyValidationError, self).__init__(detail=detail, code=code)


class MyAPIException(APIException):
    """
    detail 只返回string
    """
    status_code = status.HTTP_200_OK
    default_detail = _('A server error occurred.')
    default_code = 'error'
    err_code = status.HTTP_200_OK

    def __init__(self, detail=None, err_code=None):
        logger.error('APIException detail:{} code:{}'.format(detail, err_code))
        if err_code:
            self.err_code = err_code
        super(MyAPIException, self).__init__(
            detail=detail, code=self.status_code)


def custom_view_exception_handler(exc, context):
    """
    处理views中的异常, 视图函数只返回200，errmsg/errcode

    exc.detail
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

    :param exc: APIException
    :param context:
    :return:
    """
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if not response:
        return response
    # 保存错误码.
    if hasattr(exc, 'err_code'):
        response.data['errcode'] = exc.err_code
        response.status_code = status.HTTP_200_OK
    if 'detail' in response.data:
        detail = response.data.pop('detail')
        if detail:
            response.data['errmsg'] = detail
    return response


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    code = ComCodeChoice.API_ERR
    msg = "{}".format(exc)
    if isinstance(exc, Http404):
        code = ComCodeChoice.API_NOT_FUND
    elif isinstance(exc, NotAuthenticated):
        # 401
        code = ComCodeChoice.UNAUTHORIZED_ERR
    elif isinstance(exc, AuthenticationFailed):
        # 401
        code = ComCodeChoice.UNAUTHORIZED_ERR
    elif isinstance(exc, PermissionDenied):
        # 403
        code = ComCodeChoice.FORBIDDEN_ERR
    logger.error(msg, exc_info=True)
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}
        set_rollback()
        return done(
            code=code,
            describe=ComCodeChoice.choices_map[code],
            errors=data,
        )
    return done(code=code, describe=msg)


def com_exception_handler(exc, context):
    """
    处理views中的异常, 视图函数只返回200，errmsg/errcode

    exc.detail
        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

    :param exc: APIException
    :param context:
    :return:
    """
    response = exception_handler(exc, context)
    return response
