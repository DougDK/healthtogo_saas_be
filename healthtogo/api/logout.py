from healthtogo.api.base import H2gResourceView


class LogOut(H2gResourceView):
    _name = 'auth_log_out'
    _uri = '/apy/logout'

    def post(self):
        return '', 200