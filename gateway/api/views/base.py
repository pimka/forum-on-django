from logging import getLogger
from rest_framework.views import APIView


class BaseView(APIView):
    logger = None
    __format = '{method} | {content_type} | {message}'

    def exception(self, request, message):
        self.logger.exception(self.__format.format(
            method = request.method,
            content_type = request.content_type,
            message = message
        ))

    def info(self, request, message):
        self.logger.info(self.__format.format(
            method = request.method,
            content_type = request.content_type,
            message = message
        ))

    def json_for_statistic(self, request, operation, before=None, after=None):
        return {
            'user_uuid' : request.auth.get('uuid') if bool(request.auth) else '',
            'operation' : operation,
            'before_changes' : before,
            'after_changes' : after
        }