# Day 1: Practice Exercises

"""
Day 1 Practice Questions:
1. Print a welcome card with your name, target role, and learning goal.
2. Store basic user profile data (name, age, is_employed, skills_list) and display their types.
3. Calculate Simple Interest: SI = (P * R * T) / 100
4. Convert temperature from Celsius to Fahrenheit: F = (C * 9/5) + 32
"""

def main():
    print("========================================")
    print("        Day 1: Practice Exercises       ")
    print("========================================")

    # Exercise 1: Welcome message
    print("\n--- Exercise 1: Welcome ---")
    user_name = input("Enter your name: ")
    print(f"Welcome to the Python Fullstack Journey, {user_name}!")

    # Exercise 2: Simple Interest Calculator
    print("\n--- Exercise 2: Simple Interest Calculator ---")
    principal = float(input("Enter principal amount: "))
    rate = float(input("Enter annual interest rate (%): "))
    time = float(input("Enter time in years: "))
    
    simple_interest = (principal * rate * time) / 100
    print(f"Calculated Simple Interest: {simple_interest:.2f}")

    # Exercise 3: Celsius to Fahrenheit
    print("\n--- Exercise 3: Temperature Converter ---")
    celsius = float(input("Enter temperature in Celsius: "))
    fahrenheit = (celsius * 9 / 5) + 32
    print(f"{celsius}°C is equal to {fahrenheit:.2f}°F")


if __name__ == "__main__":
    main()
