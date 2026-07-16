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
                "username": "Maxxx1",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Maxxx1"
        assert create_user_response.json()["role"] == "ROLE_CREDIT_SECRET"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Maxxx1",
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
        credit_id = credit_request_response.json()["creditId"]

        credit_repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": credit_id,
                "accountId": account_id,
                "amount": 10000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        assert credit_repay_response.status_code == 200
        assert credit_repay_response.json()["creditId"] == credit_id
        assert credit_repay_response.json()["amountDeposited"] == 10000


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
                "username": "Max123123",
                "password": "Pas!sw0rd",
                "role": "ROLE_CREDIT_SECRET"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200
        assert create_user_response.json()["username"] == "Max123123"
        assert create_user_response.json()["role"] == "ROLE_CREDIT_SECRET"

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max123123",
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
        #credit_id = credit_request_response.json()["creditId"]

        credit_repay_response = requests.post(
            url="http://localhost:4111/api/credit/repay",
            json={
                "creditId": 123,
                "accountId": account_id,
                "amount": 10000
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            })
        assert credit_repay_response.status_code == 404