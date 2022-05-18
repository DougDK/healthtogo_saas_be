from healthtogo.api.base import H2gResourceView, auth
from werkzeug.security import generate_password_hash, check_password_hash

users = {
    "pac_test": generate_password_hash("test1234"),
    "nutri_test": generate_password_hash("test1234")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

class LogIn(H2gResourceView):
    _name = 'auth_log_in'
    _uri = '/apy/login'

    @auth.login_required
    def post(self):
        return 'LOGIN SUCCESSFUL', 200