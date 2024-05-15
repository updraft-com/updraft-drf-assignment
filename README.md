# Updraft Technical Test Guide

Welcome to Updraft's technical test. This README file serves as a comprehensive guide to set up your development environment and complete your task. Kindly read through this entire document to grasp the objectives, expectations, and resources provided.

> ⚠️ Important Notice: Please refrain from sharing your solutions on GitHub or other publicly accessible internet spaces. This ensures fair play for all future applicants and maintains the integrity of this test.
>
> We realise this sounds like an unlikely form of plagerism to occur, but Google
> is powerful and trust us: this is exactly how at least one engineer at Updraft
> used to find the answers to their university coursework... 🤷‍♂️

## Introduction

This test involves a Django web service configured with the Django REST framework. Your objective is to create both list and retrieve endpoints for the Account and Transaction models while following best practices.

## Getting set up

Before getting started with the main tasks, you'll need to configure your
development environment and make sure the tests pass.

1. create a python 3 virtual environment
2. install dependencies with poetry
3. run the tests

## Create a Python 3 virtual environment

To get started, set up a Python 3 virtual environment. You may use any modern Python 3 version for this task. If you're unsure about virtual environments, the following commands should suffice:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies with poetry

We use [`poetry`](https://python-poetry.org/) to manage python dependencies, if
you don't have it installed globally then you can install it in your venv using
pip like so:

```bash
pip install poetry
```

Now you can use it to install all of the dependencies:

```bash
poetry install
```

If you need to add a new library to the project, you can do so like this:

```bash
poetry add [--dev] <library>
```

This updates the `pyproject.toml` and `poetry.lock` files, ensuring that we evaluate your solution under the same conditions.

## Sample (fixture) data

Fixture data is provided to simulate a real-world scenario.
The data includes three users:

1. Superuser "test-admin" for Django admin panel access
2. Regular user "user1" with two bank accounts
3. Regular user "user2" with one bank account

Each user's password is the same as their username.

To load the sample data, ensure that your venv is active and then run all of the
database migrations and load the data using `manage.py`:

```bash
python manage.py migrate
python manage.py loaddata sample.json
```

Now if you run the server and browse to the admin panel
(http://localhost:8000/admin) log in as "test-admin" (password is also
"test-admin") you should see the three accounts and 419 sample transactions.

If you want to make use of this fixture data in any tests you write, be sure to
set the `fixtures` property of your `APITestCase` subclass:

```python
class TestSomething(APITestCase):

    fixtures = ["sample.json"]

    def test_something(self):
        # there are three accounts in the fixture data
        assert Accounts.objects.count() == 3
```

## Run the tests

We use [`pytest`](https://pytest.org/) to run our tests:

```bash
pytest
```

You should see all tests failing, as the endpoints that they are testing have
not been implemented. As you work on your task, you may wish to add more tests
to ensure that you're covering all the important scenarios.

## Your task

You will need to create both list and retrieve endpoints for the `Account` and
`Transaction` models.

When building these endpoints, we encourage you to develop a solution that you
would consider to be clean, maintainable and uses Django REST framework's
built-in tools to fullfil the requirements. This exercise is less about "just
build something that works" and more "show us how you woud build this in a
larger production app." Django REST framework gives you a lot of tools out of
the box and we'd like you to use this as an opportunity to demonstrate your
knowledge of those tools to us.

The following API endpoints are expected to be supported:

- `GET /accounts/` - list all bank accounts
- `GET /accounts/:id` - Retrieves a specific bank account by `:id`
- `GET /transactions/` - list all transactions
- `GET /transactions/:id` - retireve the transactions by `:id`

Users should only see their own Accounts and Transactions, while admin users (User.is_staff) should see all.
Implement cursor-based pagination for all list endpoints.
Enable filtering for transactions by timestamps, account IDs, and transaction categories.
Extend the Account model to include transaction_count_last_thirty_days and balance_change_last_thirty_days.

Additionally, these endpoints should meet the following requirements:

1. Users should only be able to see their own `Account`s and `Transaction`s,
   whilst an admin (`User.is_staff`) should be able to view all accounts and transactions in the system.
2. All "list" endpoints should be paginated using cursor-based pagination.
3. The `Transaction`s list endpoint should be ordered with the most recent
   transactions first and allow a user to filter by:
   - a start and/or end timestamp
   - the ID of one of their accounts
   - a transaction category (see `accounts.models.TransactionCategory`)
4. The `Account` endpoints should include two fields that are not part of the
   normal `Account` model:
   - `transaction_count_last_thirty_days` which should be the count of all
     `Transaction`s that occured on this account in the last 30 days.
   - `balance_change_last_thirty_days` which should be the sum of all
     `Transaction`s that occurred on this account in the last 30 days.

An `Account` object should be represented like this when returned as part of an
API response:

```json
{
    "id": 1,
    "user": 2,
    "name": "John Smith",
    "transaction_count_last_thirty_days": 119,
    "balance_change_last_thirty_days": "-1304.67",
}
```

(Note: the fields that calculate values for the last thirty days will change
values depending which day you actually do this test. Don't worry if yours come
out different. See `TestAccountsApiAsStaff::test_retrieve_account` in
`accounts/tests.py` for a way to fix this during testing with the `freeze_time`
annotation from the [freezegun](https://github.com/spulec/freezegun) package)

A `Transaction` object should be represented like this:

```json
{
    "id": 1,
    "account": 1,
    "timestamp": "2022-06-12T17:36:58.632000Z",
    "amount": "-25.26",
    "description": "Tesco",
    "transaction_category": "PURCHASE"
}
```
