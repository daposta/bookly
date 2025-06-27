from src.auth.schemas import UserSignupRequest

auth_prefix = "/api/v1/auth"
def test_signup(fake_session, fake_user_service, test_client):
    signup_data = {
        "username": "dayton",
         "first_name": "secret",
        "last_name": "secret",
        "email" : "dayton@gmail.com",
        "password": "secret2345"

    }

    user_data= UserSignupRequest(**signup_data)
    response = test_client.post(url=f"{auth_prefix}/signup", json=signup_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(signup_data["email"], fake_session)
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data, fake_session)

    # assert response.status_code == 201
