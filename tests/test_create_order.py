import allure
import data
from conftest import default_user
from conftest import default_burger

class TestCreateOrder:
    @allure.title("Проверка успешного создания авторизованным пользователем")
    def test_create_order_authorized_user(self, default_burger, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        create_response = data.create_new_order(headers, default_burger)
        assert create_response.status_code == 200 and create_response.json()["order"]["number"] != None

    @allure.title("Проверка ошибки при пустом заказе авторизованного пользователя")
    def test_create_without_order_authorized_user(self, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        create_response = data.create_new_order(headers, None)
        assert create_response.status_code == 400 and create_response.json()["message"] == data.MES_ORDER_WITHOUT_DATA_AUTH


    @allure.title("Провека ошибки при заказе неавторизованным пользователем")
    @allure.description("Без авторизация нельзя создать заказ.")
    def test_create_order_without_authorized_user(self, default_burger):
        create_response = data.create_new_order(None, None)
        assert create_response.status_code == 400


    @allure.title("Проверка ошибка при заказе авторизованным пользователем с неверным хешем")
    @allure.description("При попытке сделать заказ авторизованным пользователем ингридиенты с невернымм хешем, возвращается ошибка 500.")
    def test_create_order_not_true_hash_authorized_user(self, default_user):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        ingredients = data.INCORRECT_INGREDIENTS
        create_response = data.create_new_order(headers, ingredients)
        assert create_response.status_code == 500

    @allure.title("Проверка ошибки при заказе неавторизованным пользователем с неверным хешем ")
    @allure.description("При попытке сделать заказ авторизованным пользователем ингридиенты с невернымм хешем, возвращается ошибка 500.")
    def test_create_order_not_true_hash_withot_authorized_user(self):
        ingredients = data.INCORRECT_INGREDIENTS
        create_response = data.create_new_order(None, ingredients)
        assert create_response.status_code == 500
