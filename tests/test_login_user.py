import allure
import pytest

import data


class TestLoginUser:
    @allure.title("Проверка успешной авторизация ранее созданного пользователя")
    @allure.description("Авторизация с полным пакетом данных")
    def test_login_user(self):
        user_data = data.create_user_body()
        user_response = data.create_user(user_data)
        user_data.pop("name", None)
        login_response = data.login_user(user_data)
        access_token = data.get_access_token(user_response)
        data.delete_user(access_token)
        assert login_response.status_code == 200 and login_response.json()["success"] == True

    @allure.title("Проверка ошибки при авторизовации без полей: - email; -password.")
    @allure.description("Возвращения ошибки при авторизации без обязательных полей.")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", ""),
                                 ("password", "")
                             ])
    def test_login_without_required_field(self, key, value):
        user_data = data.create_user_body()
        user_response = data.create_user(user_data)
        login_data = user_data.copy()
        login_data[key] = value
        login_data.pop("name", None)
        login_response = data.login_user(login_data)
        access_token = data.get_access_token(user_response)
        data.delete_user(access_token)
        assert login_response.status_code == 401 and login_response.json()["message"] == data.MES_INCORRECT_FIELDS

