import allure
import data
from conftest import default_user
from conftest import default_burger



class TestReceivUserOrders:
    @allure.title("Проверка получения списка заказов авторизованного пользователя")
    @allure.description("получили cписок заказов авторизованного пользователя")
    def test_reseiv_orders_authorization_user(self, default_user, default_burger):
        user_response, access_token = default_user
        headers = {"Authorization": access_token}
        ingredients = default_burger
        data.create_new_order(headers, ingredients)
        data.create_new_order(headers, ingredients)
        user_orders = data.get_users_orders(headers)
        assert user_orders.status_code == 200
        assert user_orders.json()["orders"][0] != None
        assert user_orders.json()["orders"][1] != None

    @allure.title("Провека ошибки 401 при получении списка заказов неавторизованным пользователем")
    @allure.description("Ошибка cписка заказов неавторизованного пользователя")
    def test_reseiv_orders_without_authorization_user(self, default_burger):
        ingredients = default_burger
        data.create_new_order(None, ingredients)
        data.create_new_order(None, ingredients)
        orders_response = data.get_users_orders(None)
        assert orders_response.status_code == 401
        assert orders_response.json()["message"] == data.MES_WITHOT_REC
