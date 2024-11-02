import allure
import requests
from conftest import default_burger
import data
import urls
import pytest


class TestModificationUsData:
    @allure.title("Проверка изменения данных пользовантеля с авторизацией")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "user123@ya.ru"),
                                 ("name", "User User"),
                                 ("password", "123456")
                             ])
    def test_modification_data_existing_user(self, key, value):
        user_data = data.create_user_body()
        data.create_user(user_data)
        body_data = user_data.copy()
        body_data.pop("name", None)
        login_response = data.login_user(body_data)
        access_token = data.get_access_token(login_response)
        body_data[key] = value
        change_response = data.change_user_data(access_token, body_data)
        data.delete_user(access_token)
        assert change_response.status_code == 200 and change_response.json()["success"] == True

    @allure.title("Проверка изменения данных пользователя без авторизации(невозможно)")
    @pytest.mark.parametrize("key, value",
                             [
                                 ("email", "User321123@ya.ru"),
                                 ("name", "User User"),
                                 ("password", "111111")
                             ])
    def test_modification_data_not_existing_user(self, key, value):
        user_data = data.create_user_body()
        create_response = data.create_user(user_data)
        body_data = user_data.copy()
        body_data[key] = value
        change_response = requests.patch(urls.START_URL + urls.URL_END_US, json=body_data)
        access_token = data.get_access_token(create_response)
        data.delete_user(access_token)
        assert change_response.status_code == 401 and change_response.json()["message"] == data.MES_WITHOT_REC
