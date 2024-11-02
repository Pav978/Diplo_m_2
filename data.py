import allure
import urls
import requests
import data_2

@allure.step("Создать тело запроса создания юзера: email, password, name")
def create_user_body():
    return data_2.new_user_login_password()

@allure.step("Создать пользователя в приложении Stellar burger")
def create_user(user_data):
    user_response = requests.post(urls.START_URL+urls.URL_CREATE_USER, json=user_data)
    return user_response

@allure.step("Получить access token созданного пользователя")
def get_access_token(user_response):
    access_token = user_response.json().get("accessToken")
    return access_token

@allure.step("Удалить созданного пользователя")
def delete_user(access_token):
    headers = {"Authorization": access_token}
    response_delete = requests.delete(urls.START_URL + urls.URL_END_US, headers=headers)
    return response_delete

@allure.step("Авторизоваться в приложении Stellar burger")
def login_user(login_data):
    login_response = requests.post(urls.START_URL + urls.URL_LOGIN, json=login_data)
    return login_response

@allure.step("Изменить данные пользователя: email, password, name")
def change_user_data(access_token, new_data):
    headers = {"Authorization": access_token}
    change_data_response = requests.patch(urls.START_URL + urls.URL_END_US, headers=headers, json=new_data)
    return change_data_response

@allure.step("Получить refreshtoken созданного пользователя")
def get_refresh_token(user_response):
    refresh_token = user_response.json().get("refreshToken")
    return refresh_token

@allure.step("Получить список доступных ингредиентов")
def get_ingredients():
    response = requests.get(urls.START_URL + urls.URL_REC_ING)
    return response

@allure.step("Создать заказ")
def create_new_order(headers, ingredients):
    response = requests.post(urls.START_URL + urls.URL_REC_ORDER, headers=headers, json=ingredients)
    return response

@allure.step("Получить все заказы конкретного пользователя")
def get_users_orders(headers):
    response = requests.get(urls.START_URL + urls.URL_REC_ORDER, headers=headers)
    return response



MES_ORDER_WITHOUT_DATA_AUTH = "Ingredient ids must be provided"
MES_WITHOT_REC = "You should be authorised"
MES_USER_GENERATED = "User already exists"
MES_REQUIRED_FIELDS = "Email, password and name are required fields"
MES_INCORRECT_FIELDS = "email or password are incorrect"
INCORRECT_INGREDIENTS = {"ingredients": ["123456qwerty654321","987654321qwertytrewq"]}
