import allure
import pytest
import data

@allure.step("Создаем курьера")
@pytest.fixture(scope='function')
def default_user():
    user_body = data.create_user_body()
    user_response = data.create_user(user_body)
    access_token = data.get_access_token(user_response)
    yield user_response, access_token
    data.delete_user(access_token)


@allure.step("Создать бургер из имеющихся ингридиентов")
@pytest.fixture(scope='function')
def default_burger():
    ingredients = data.get_ingredients().json()
    ingredient_types = {"main": None, "sause": None, "bun": None}
    for item in ingredients["data"]:
        if item["type"] in ingredient_types and ingredient_types[item["type"]] is None:
            ingredient_types[item["type"]] = item["_id"]
    burger_ingredient = {"ingredients": list(ingredient_types.values())}
    return burger_ingredient

