class MethodLogger:
    def __getattribute__(self, name):
        value = super().__getattribute__(name)
        if callable(value) and not name.startswith('__'):
            def logger(*args, **kwargs):
                print(f"Calling method: {name} with: {args}, {kwargs}")
                return value(*args, **kwargs)
            return logger
        return value


class User(MethodLogger):
    total_users = 0

    def __init__(self, username: str, email: str, country: str, wallet_balance: float):
        self._username = username
        self._email = email
        self._country = country
        self._payment_methods = []
        self._wallet_balance = wallet_balance
        User.total_users += 1

    def __str__(self):
        return f"User: {self._username}, Email: {self._email}, Country: {self._country}, Wallet: {self._wallet_balance}$"

    def add_payment_method(self, payment_method):
        self._payment_methods.append(payment_method)

    def view_payment_methods(self):
        return [str(m) for m in self._payment_methods]

    def check_funds(self, amount: float) -> bool:
        return self._wallet_balance >= amount

    def deduct_funds(self, amount: float):
        if self.check_funds(amount):
            self._wallet_balance -= amount
        else:
            raise ValueError("Insufficient funds!")

    @staticmethod
    def total_users_count():
        return User.total_users

    def set_data(self, username, wallet_balance):
        self._username = username
        self._wallet_balance = wallet_balance


class PremiumUser(User):
    def __init__(self, username: str, email: str, country: str, wallet_balance: float, membership_level: str):
        super().__init__(username, email, country, wallet_balance)
        self._membership_level = membership_level

    def __str__(self):
        return f"Premium User: {self._username}, Level: {self._membership_level}, Wallet: {self._wallet_balance}$"


class Game(MethodLogger):
    total_games = 0

    def __init__(self, name: str, price: float, category: str):
        self._name = name
        self._price = price
        self._category = category
        self._owners = []
        Game.total_games += 1

    def __str__(self):
        return f"Game: {self._name}, Price: {self._price}$, Category: {self._category}"

    def add_owner(self, user: User):
        self._owners.append(user)

    def apply_discount(self, discount: float):
        if 0 < discount < 1:
            self._price *= (1 - discount)
        else:
            raise ValueError("Discount must be between 0 and 1")

    @staticmethod
    def total_games_count():
        return Game.total_games


class PremiumGame(Game):
    def __init__(self, name: str, price: float, category: str, exclusive_content: bool):
        super().__init__(name, price, category)
        self._exclusive_content = exclusive_content

    def __str__(self):
        content_status = "with exclusive content" if self._exclusive_content else "without exclusive content"
        return f"Premium Game: {self._name}, Price: {self._price}$, {content_status}"


class Transaction(MethodLogger):
    total_transactions = 0

    def __init__(self, user: User, game: Game, payment_method):
        self._user = user
        self._game = game
        self._payment_method = payment_method
        Transaction.total_transactions += 1

    def __str__(self):
        return f"Transaction: User: {self._user._username}, Game: {self._game._name}, Payment Method: {self._payment_method}"

    @staticmethod
    def total_transactions_count():
        return Transaction.total_transactions


class PaymentMethod:
    def __init__(self, method: str):
        self._method = method

    def __str__(self):
        return f"Payment Method: {self._method}"

class Discount:
    def __init__(self, discount_rate: float):
        self._discount_rate = discount_rate

    def apply_discount(self, price: float):
        return price * (1 - self._discount_rate)


class PremiumDiscountedUser(PremiumUser, Discount):
    def __init__(self, username: str, email: str, country: str, wallet_balance: float, membership_level: str, discount_rate: float):
        PremiumUser.__init__(self, username, email, country, wallet_balance, membership_level)
        Discount.__init__(self, discount_rate)

    def __str__(self):
        return f"Premium Discounted User: {self._username}, Level: {self._membership_level}, Discount: {self._discount_rate*100}%"


class GameStore(MethodLogger):
    def __init__(self, name: str):
        self._name = name
        self._games = []
        self._users = []

    def __str__(self):
        return f"Game Store: {self._name}"

    def add_game(self, game: Game):
        self._games.append(game)

    def register_user(self, user: User):
        self._users.append(user)

    def list_games(self):
        return [str(game) for game in self._games]

    def list_users(self):
        return [str(user) for user in self._users]

    def purchase_game(self, user: User, game: Game):
        if user.check_funds(game._price):
            user.deduct_funds(game._price)
            game.add_owner(user)
            return Transaction(user, game, "Wallet")
        else:
            print(f"{user._username} does not have enough funds to purchase {game._name}!")



def print_user_info(user: User):
    print(user)

def main():
    store = GameStore("Steam")
    print(store)

    game1 = Game("Cyberpunk 2077", 60.0, "RPG")
    game2 = Game("The Witcher 3", 40.0, "RPG")
    game3 = PremiumGame("Hades", 20.0, "Action", exclusive_content=True)
    store.add_game(game1)
    store.add_game(game2)
    store.add_game(game3)
    print("Available games:", store.list_games())

    user1 = User("player_one", "player1@mail.com", "USA", wallet_balance=50.0)
    store.register_user(user1)
    print("Registered users:", store.list_users())

    premium_user = PremiumUser("elite_gamer", "elite@mail.com", "Canada", wallet_balance=100.0, membership_level="Gold")
    store.register_user(premium_user)
    print("Registered users:", store.list_users())

    discounted_user = PremiumDiscountedUser("super_elite", "elite@mail.com", "Canada", wallet_balance=100.0, membership_level="Gold", discount_rate=0.15)
    store.register_user(discounted_user)
    print("Registered users:", store.list_users())

    payment_method = PaymentMethod("PayPal")
    user1.add_payment_method(payment_method)
    premium_user.add_payment_method(payment_method)
    print("User payment methods:", user1.view_payment_methods())

    print(f"\nAttempting to purchase {game1._name} for {user1._username}:")
    transaction = store.purchase_game(user1, game1)
    print(transaction)

    print(f"\nAttempting to purchase {game3._name} for {premium_user._username}:")
    transaction = store.purchase_game(premium_user, game3)
    print(transaction)

    original_price = 60.0
    discounted_price = discounted_user.apply_discount(original_price)
    print(f"Original Price: {original_price}$, Discounted Price: {discounted_price}$")

    print(f"Total Users: {User.total_users_count()}")
    print(f"Total Games: {Game.total_games_count()}")
    print(f"Total Transactions: {Transaction.total_transactions_count()}")


if __name__ == "__main__":
    main()
