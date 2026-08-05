from app.core.supabase import supabase

class AuthService:

    def signup(self, email: str, password: str):
        return supabase.auth.sign_up(
            {
                "email": email,
                "password": password,
            }
        )

    def login(self, email: str, password: str):
        return supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password,
            }
        )

auth_service = AuthService()
    