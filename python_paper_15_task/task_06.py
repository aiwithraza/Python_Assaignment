from dataclasses import dataclass


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    action: str
    amount: float
    balance_after: float


def check_amount(amount):
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise TypeError("Amount must be a number")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")


class Account:
    def __init__(self, account_id, opening_balance=0):
        if isinstance(opening_balance, bool) or not isinstance(opening_balance, (int, float)):
            raise TypeError("Opening balance must be a number")
        if opening_balance < 0:
            raise ValueError("Opening balance cannot be negative")

        self._account_id = account_id
        self._balance = 0
        self._transactions = []

        if opening_balance > 0:
            self._balance = opening_balance
            self._record("opening balance", opening_balance)

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):
        return self._balance

    def _record(self, action, amount):
        number = len(self._transactions) + 1
        record = Transaction(f"{self._account_id}-{number}", action, amount, self._balance)
        self._transactions.append(record)

    def deposit(self, amount, action="deposit"):
        check_amount(amount)
        self._balance += amount
        self._record(action, amount)

    def withdraw(self, amount, action="withdrawal"):
        check_amount(amount)
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._record(action, amount)

    def statement(self):
        return tuple(self._transactions)


class Bank:
    def __init__(self):
        self._accounts = {}

    def create_account(self, account_id, opening_balance=0):
        if account_id in self._accounts:
            raise ValueError(f"Account '{account_id}' already exists")
        account = Account(account_id, opening_balance)
        self._accounts[account_id] = account
        return account

    def get_account(self, account_id):
        if account_id not in self._accounts:
            raise ValueError(f"Account '{account_id}' does not exist")
        return self._accounts[account_id]

    def deposit(self, account_id, amount):
        self.get_account(account_id).deposit(amount)

    def withdraw(self, account_id, amount):
        self.get_account(account_id).withdraw(amount)

    def transfer(self, from_id, to_id, amount):
        source = self.get_account(from_id)
        target = self.get_account(to_id)
        if source is target:
            raise ValueError("Cannot transfer to the same account")

        check_amount(amount)
        if amount > source.balance:
            raise ValueError("Insufficient funds")

        source.withdraw(amount, f"transfer out to {to_id}")
        target.deposit(amount, f"transfer in from {from_id}")


def print_statement(account):
    print(f"Statement for account {account.account_id}")
    for t in account.statement():
        print(f"  {t.transaction_id:<6} {t.action:<20} {t.amount:>8}  balance: {t.balance_after}")


def main():
    bank = Bank()
    bank.create_account("A", 1000)
    bank.create_account("B", 200)

    bank.transfer("A", "B", 350)
    print("After transfer -> A:", bank.get_account("A").balance,
          "B:", bank.get_account("B").balance)

    bank.deposit("A", 100)
    bank.withdraw("B", 50)

    bad_actions = [
        lambda: bank.transfer("A", "B", 99999),
        lambda: bank.transfer("A", "Z", 10),
        lambda: bank.deposit("A", -5),
        lambda: bank.withdraw("B", 0),
    ]
    for action in bad_actions:
        try:
            action()
        except (ValueError, TypeError) as error:
            print("Error:", error)

    print("Balances now -> A:", bank.get_account("A").balance,
          "B:", bank.get_account("B").balance)
    print_statement(bank.get_account("A"))
    print_statement(bank.get_account("B"))


if __name__ == "__main__":
    main()