import pytest
import requests


@pytest.mark.api
class TestTransferBetweenAccount:
    def test_valid_transfer(self):
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
                "username": "Max11123",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max11123",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

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
                "amount": 8000.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",

            }
        )

        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 8000.5

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

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={"fromAccountId": first_account_id,
                  "toAccountId": second_account_id,
                  "amount": 5000.5},
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })
        assert transfer_response.status_code == 200
        assert transfer_response.json().get("fromAccountIdBalance") == 3000

    def test_invalid_transfer(self):
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
                "username": "Max11112233",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max11112233",
                "password": "Pas!sw0rd"
            },
            headers={
                "Content-Type": "application/json",
                "accept": "application/json"
            }
        )
        assert login_user_response.status_code == 200
        token = login_user_response.json().get("token")

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
                "amount": 5000.5
            },
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",

            }
        )

        assert deposit_account_response.status_code == 200
        assert deposit_account_response.json().get("balance") == 5000.5

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

        transfer_response = requests.post(
            url="http://localhost:4111/api/account/transfer",
            json={"fromAccountId": first_account_id,
                  "toAccountId": second_account_id,
                  "amount": 8000.5
                  },
        headers={
            "accept": "application/json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        })
        assert transfer_response.status_code == 422
