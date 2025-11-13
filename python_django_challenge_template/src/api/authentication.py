from rest_framework_simplejwt.authentication import JWTAuthentication


class UserKeyJWTAuthentication(JWTAuthentication):
  def get_header(self, request):
    user_key = request.headers.get('USER-KEY')
    if user_key is None:
      return None
    
    return user_key
  
  def authenticate(self, request):
        """
        Override to allow JWTAuthentication to process USER-KEY.
        """
        header = self.get_header(request)
        if header is None:
            return None
        
        raw_token = header.split()[1] if ' ' in header else header

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return (user, validated_token)