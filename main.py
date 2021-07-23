from decimal import Decimal
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from bankaccounts.application import BankAccounts

app = FastAPI()
accounts = BankAccounts()


class AccountDetails(BaseModel):
    full_name: str
    email_address: str
    balance: Decimal
    overdraft_limit: Decimal
    is_closed: bool


@app.get("/accounts/{account_id}", response_model=AccountDetails)
async def get_account(account_id: UUID):
    try:
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account.__dict__


@app.post("/accounts")
async def open_account(full_name: str, email_address: str):
    try:
        account_id = accounts.open_account(full_name, email_address)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account_id


@app.post("/account/{account_id}/deposit", response_model=AccountDetails)
async def deposit_funds(account_id: UUID, amount: Decimal):
    try:
        accounts.deposit_funds(
            credit_account_id=account_id,
            amount=amount,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account.__dict__


@app.post("/account/{account_id}/withdraw", response_model=AccountDetails)
async def withdraw_funds(account_id: UUID, amount: Decimal):
    try:
        accounts.withdraw_funds(
            debit_account_id=account_id,
            amount=amount,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account.__dict__


@app.post("/account/{account_id}/transfer", response_model=AccountDetails)
async def transfer_funds(account_id: UUID, to_account_id: UUID, amount: Decimal):
    try:
        accounts.transfer_funds(
            debit_account_id=account_id,
            credit_account_id=to_account_id,
            amount=amount,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account.__dict__


@app.post("/account/{account_id}/overdraft", response_model=AccountDetails)
async def set_overdraft_limit(account_id: UUID, limit: Decimal):
    try:
        accounts.set_overdraft_limit(
            account_id=account_id,
            overdraft_limit=limit,
        )
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account.__dict__


@app.post("/account/{account_id}/close", response_model=AccountDetails)
async def close_account(account_id: UUID):
    try:
        accounts.close_account(account_id)
        account = accounts.get_account(account_id)
    except Exception as e:
        return {"error": e.__class__.__name__}
    return account.__dict__


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
