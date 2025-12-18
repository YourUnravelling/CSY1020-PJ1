"""
inp = input().split(" ")
flt_inp = []
for item in inp:
    flt_inp.append(float(item))
total = 0.0
highest = 0.0
for value in flt_inp:
    total += value
    if value > highest:
        highest = value
avg = total/len(inp)
"""

"""
class Car:

    def __init__(self):
        self.model_year = 0
        self.purchase_price:int # TODO: Declare purchase_price attribute

        self.current_value = 0

    def calc_current_value(self, current_year):
        depreciation_rate = 0.15
        # Car depreciation formula
        car_age = current_year - self.model_year
        self.current_value = round(self.purchase_price *
                                   (1 - depreciation_rate)**car_age)

    # TODO: Define print_info() method to output model_year, purchase_price, and current_value
    def print_info(self):
        print(f"Car's information:\n  Model year: {self.model_year}\n  Purchase price: ${self.purchase_price}\n  Current value: ${self.current_value}")


if __name__ == "__main__":
    year = int(input())
    price = int(input())
    current_year = int(input())

    my_car = Car()
    my_car.model_year = year
    my_car.purchase_price = price
    my_car.calc_current_value(current_year)
    my_car.print_info()
"""
"""
class FoodItem:
    # TODO: Define constructor with parameters to initialize instance
    #       attributes (name, fat, carbs, protein)
    def __init__(self, name="Water", fat=0.0, carbs=0.0, protein=0.0):
        self.name = name
        self.fat = fat
        self.carbs = carbs
        self.protein = protein

    def get_calories(self, num_servings):
        # Calorie formula
        calories = ((self.fat * 9) + (self.carbs * 4) +
                    (self.protein * 4)) * num_servings
        return calories

    def print_info(self):
        print(f"Nutritional information per serving of {self.name}:")
        print(f"  Fat: {self.fat:.2f} g")
        print(f"  Carbohydrates: {self.carbs:.2f} g")
        print(f"  Protein: {self.protein:.2f} g")


if __name__ == "__main__":

    item_name = input()
    if item_name == "Water" or item_name == "water":
        food_item = FoodItem()
        food_item.print_info()
        print(
            f"Number of calories for {1.0:.2f} serving(s): {food_item.get_calories(1.0):.2f}"
        )

    else:
        amount_fat = float(input())
        amount_carbs = float(input())
        amount_protein = float(input())
        num_servings = float(input())

        food_item = FoodItem(item_name, amount_fat, amount_carbs,
                             amount_protein)
        food_item.print_info()
        print(
            f"Number of calories for {1.0:.2f} serving(s): {food_item.get_calories(1.0):.2f}"
        )
        print(
            f"Number of calories for {num_servings:.2f} serving(s): {food_item.get_calories(num_servings):.2f}"
        )
"""

"""
class Artist:
    # TODO: Define constructor with parameters to initialize instance attributes
    #       (name, birth_year, death_year)
    def __init__(self, name="unknown", birth_year=-1, death_year=-1):
        self.name = name
        self.birth_year = birth_year
        self.death_year = death_year

    # TODO: Define print_info() method
    def print_info(self):
        if self.birth_year > 0 and self.death_year > 0:
            print(f"Artist: {self.name} ({self.birth_year} to {self.death_year})")
        elif self.birth_year > 0 and self.death_year < 0:
            print(f"Artist: {self.name} ({self.birth_year} to present)")
        else:
            print(f"Artist: {self.name} (unknown)")



      
class Artwork:
    # TODO: Define constructor with parameters to initialize instance attributes
    #       (title, year_created, artist)
    def __init__(self, title="unknown", year_created=-1, artist=Artist()):
        self.title = title
        self.year_created = year_created
        self.artist = artist

    # TODO: Define print_info() method
    def print_info(self):
        self.artist.print_info()
        print(f"Title: {self.title}, {self.year_created}")



if __name__ == "__main__":
    user_artist_name = input()
    user_birth_year = int(input())
    user_death_year = int(input())
    user_title = input()
    user_year_created = int(input())

    user_artist = Artist(user_artist_name, user_birth_year, user_death_year)

    new_artwork = Artwork(user_title, user_year_created, user_artist)

    new_artwork.print_info()
"""


SALES_TAX = 0.07

class SelfPayKiosk:

    # Constructor
    def __init__(self):
        # Complete the constructor
        self.num_customers = 0
        self.total_sales = 0
        self.current_amount_due = 0.0

    # Return total daily sales
    def get_total_sales(self):
        # Update the return statment
        return self.total_sales

    # Return current amount due
    def get_amount_due(self):
        # Update the return statment
        return self.current_amount_due

    # Return number of customers served
    def get_num_customers(self):
        return self.num_customers -1

    # Scan one item
    def scan_item(self, price):
        if price < 0:
            self.current_amount_due += price

    # Apply sales tax to current purchases
    def check_out(self):
        self.current_amount_due += self.current_amount_due * SALES_TAX

    # Cancel current purchases
    def cancel_transaction(self):
        self.current_amount_due = 0

    # Reset register for the day
    def reset_kiosk(self):
        self.current_amount_due = 0
        self.num_customers = 0
        self.total_sales = 0

    # Apply payment to amount due
    def make_payment(self, payment):
        if payment < 0: return
        if payment >= self.current_amount_due:
            self.total_sales += self.current_amount_due
            self.num_customers += 1
            self.current_amount_due = 0.0
        else:
            self.total_sales += payment
            self.current_amount_due -= payment

    # Simulate multiple transactions
    def simulate_sales(self, num_sales, initial_price, incr_price):
        for i in range(num_sales):
            self.scan_item(initial_price)
            self.check_out()
            self.make_payment(self.current_amount_due + 1)
            self.i
        return -1


if __name__ == "__main__":
    kiosk = SelfPayKiosk()

    # Test basic operations
    kiosk.scan_item(20.49)
    kiosk.check_out()
    kiosk.make_payment(25.20)
    print(f"Number of customers: {kiosk.get_num_customers()}")
    print(f"Amount due: {kiosk.get_amount_due():.2f}")
    print(f"Total Sales: {kiosk.get_total_sales():.2f}")

    # Add statements as instance methods are completed to support development mode testing

    # Test simulate_sales()
    kiosk.reset_kiosk()
    kiosk.simulate_sales(100, 5, 2.5)
    print(f"Number of customers: {kiosk.get_num_customers()}")
    print(f"Amount due: {kiosk.get_amount_due():.2f}")
    print(f"Total Sales: {kiosk.get_total_sales():.2f}")
