from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackEnd(ModelBackend):
    def authenticate(self, usernameoremail=None, password=None, **kwargs):
        UserModel = get_user_model()

        try:
            if '@' in usernameoremail:
                user = UserModel.objects.get(email = usernameoremail)
            elif 'ven' in usernameoremail:
                user = UserModel.objects.get(vendor_id = usernameoremail)
            else:
                user = UserModel.objects.get(username = usernameoremail)

            if user.check_password(password):
                return user

        except UserModel.DoesNotExist:
            return None
            
        return None