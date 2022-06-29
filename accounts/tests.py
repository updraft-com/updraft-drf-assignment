from django.contrib.auth import get_user_model
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase


class TestAccountsApiAsStaff(APITestCase):

    # this line loads the fixture data with sample users, accounts and transactions
    fixtures = ["sample.json"]

    def setUp(self):
        super().setUp()
        # this user exists in the fixtures
        admin_user = get_user_model().objects.get(username="test-admin")
        self.client.force_authenticate(admin_user)

    def test_accounts_list(self):
        response = self.client.get("/accounts/")

        assert response.status_code == status.HTTP_200_OK

        # there should be a list of transactions for this page in the 'results' field
        assert len(response.json()["results"]) > 0

    # the freeze_time annotation ensures that the test always runs as if stuck at a
    # specific point in time, so assertions about the transaction_count_last_thirty_days
    # and balance_change_last_thirty_days fields will work predictably.
    @freeze_time("2022-06-14 18:00:00")
    def test_retrieve_account(self):
        response = self.client.get("/accounts/1/")

        assert response.status_code == status.HTTP_200_OK

        assert response.json() == {
            "id": 1,
            "user": 2,
            "name": "John Smith",
            "transaction_count_last_thirty_days": 119,
            "balance_change_last_thirty_days": "-1304.67",
        }
