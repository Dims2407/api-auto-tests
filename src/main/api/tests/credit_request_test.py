import requests
import pytest

@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            })
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Maxxx",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Maxxx"
        assert create_user_response.json()["role"] == "ROLE_CREDIT_SECRET"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Maxxx",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0
        account_id = create_account_response.json().get("id")

        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": account_id,
                "amount": 5000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",

            }
        )

        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 5000

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": account_id,
                "amount": 10000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert credit_request_response.status_code == 201
        assert credit_request_response.json()["amount"] == 10000
        assert credit_request_response.json()["balance"] == 15000


    def test_credit_request_invalid(self):
        login_admin_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "admin",
                "password": "123456"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            })
        assert login_admin_response.status_code == 200
        token = login_admin_response.json().get("token")

        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max111",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max111",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Max111"
        assert create_user_response.json()["role"] == "ROLE_CREDIT_SECRET"

        create_first_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_first_account_response.status_code == 201
        assert create_first_account_response.json().get("balance") == 0
        first_account_id = create_first_account_response.json().get("id")

        deposit_account_response = requests.post(
            url="http://localhost:4111/api/account/deposit",
            json={
                "accountId": first_account_id,
                "amount": 5000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",

            }
        )

        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 5000

        create_second_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_second_account_response.status_code == 201
        assert create_second_account_response.json().get("balance") == 0
        second_account_id = create_second_account_response.json().get("id")

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": first_account_id,
                "amount": 10000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert credit_request_response.status_code == 201
        assert credit_request_response.json()["amount"] == 10000
        assert credit_request_response.json()["balance"] == 15000

        credit_request_response = requests.post(
            url="http://localhost:4111/api/credit/request",
            json={
                "accountId": second_account_id,
                "amount": 10000,
                "termMonths": 12
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        assert credit_request_response.status_code == 404
