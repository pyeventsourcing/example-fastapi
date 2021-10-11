from uuid import UUID
from decimal import Decimal
from fastapi import FastAPI

from bankaccounts.application import BankAccounts

app = FastAPI()
accounts = BankAccounts()


@app.get("/accounts/{account_id}")
def get_account(account_id: UUID):
    try:
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account


@app.post("/accounts")
def open_account(full_name: str, email_address: str):
    try:
        account_id = accounts.open_account(full_name, email_address)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account_id


@app.post("/account/{account_id}/deposit")
def deposit_funds(account_id: UUID, amount: Decimal):
    try:
        accounts.deposit_funds(
            credit_account_id=account_id,
            amount=amount,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account


@app.post("/account/{account_id}/withdraw")
def withdraw_funds(account_id: UUID, amount: Decimal):
    try:
        accounts.withdraw_funds(
            debit_account_id=account_id,
            amount=amount,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account


@app.post("/account/{account_id}/transfer")
def transfer_funds(account_id: UUID, to_account_id: UUID, amount: Decimal):
    try:
        accounts.transfer_funds(
            debit_account_id=account_id,
            credit_account_id=to_account_id,
            amount=amount,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account


@app.post("/account/{account_id}/overdraft")
def set_overdraft_limit(account_id: UUID, limit: Decimal):
    try:
        accounts.set_overdraft_limit(
            account_id=account_id,
            overdraft_limit=limit,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account


@app.post("/account/{account_id}/close")
def close_account(account_id: UUID):
    try:
        accounts.close_account(account_id)
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
