import allure
import data
from data_2 import *
import pytest
from conftest import default_user


class TestCreateUser:
    @allure.title("Проверка успешной регистрации пользователя")
    @allure.description("Пользователь создан")
    def test_create_user(self, default_user):
        user_response, access_token = default_user
        assert user_response.status_code == 200 and user_response.json() is not None

    @allure.title("Проверка ошибки 403 при создании уже существующего пользователя")
    @allure.description("Создание пользователя с данными уже существующег.")
    def test_create_existing_user(self):
        body = data.create_user_body()
        user_response = data.create_user(body)
        create_duplicate_request = data.create_user(body)
        access_token = data.get_access_token(user_response)
        data.delete_user(access_token)
        assert create_duplicate_request.status_code == 403 and create_duplicate_request.json()[
            "message"] == data.MES_USER_GENERATED

    @allure.title("Проверка ошибки 403 при создании пользователя с незаполненным обязательным полем")
    @allure.description("Отправляем запрос без обязательного поля и получаем сообщение об ошибке")
    @pytest.mark.parametrize('key, value',
                             [
                                 ("email", ""),
                                 ("password", ""),
                                 ("name", "")
                             ])
    def test_create_user_without_mandatory_field(self, key, value):
        body = ChangeTestDataHelper.modify_create_user_body(key, value)
        user_response = data.create_user(body)
        assert user_response.status_code == 403 and user_response.json()["message"] == data.MES_REQUIRED_FIELDS
