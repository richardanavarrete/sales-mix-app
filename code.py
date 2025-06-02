import streamlit as st
import pandas as pd

# --- Dictionaries and Lists ---

item_to_category = {
    # Bottle Beer
    "Can Austin Cider": ["Cans / Prem Bottle"],
    "Bud Light Bottle": ["Dom Bottle"],
    "Budweiser Bottle": ["Dom Bottle"],
    "Coors Bottle": ["Dom Bottle"],
    "Coors Light Bottle": ["Dom Bottle"],
    "Michelob Ultra Bottle": ["Dom Bottle"],
    "Miller Light Bottle": ["Dom Bottle"],
    "O'Douls Bottle": ["Dom Bottle"],
    "Domestic Bucket": ["Dom Bucket"],
    "Zippa Rona": ["Zipparona"],
    "Angry Orchard Bottle": ["Cans / Prem Bottle"],
    "CAN Austin Cider ": ["Cans / Prem Bottle"], # Note: df['Item'] normalization will make this 'Can Austin Cider'
    "College Street Big Blue Van Bottle": ["Cans / Prem Bottle"],
    "Corona N/A Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Corona Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Corona Premier Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Cornonita Bucket (Zipps)": ["Coronita Bucket $24"],
    "Dos XX Lager Bottle ": ["Cans / Prem Bottle", "Mexi Bottles"], # Note: Trailing space
    "CAN Guinness ": ["Cans / Prem Bottle"],
    "CAN Heineken Zero ": ["Cans / Prem Bottle"],
    "Modelo Especial Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Pacifico": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Truly Pineapple ": ["Hard Seltzer"],
    "Truly Pineapple (Fs) ": ["Hard Seltzer"],
    "Truly Wild Berry": ["Hard Seltzer"],
    "Truly Wild Berry (Fs)": ["Hard Seltzer"],
    "CAN Twisted Tea ": ["Cans / Prem Bottle"],
    "CAN White Claw Black Cherry ": ["Hard Seltzer"],
    "CAN White Claw Black Cherry (Fs) ": ["Hard Seltzer"],
    "CAN White Claw Mango ": ["Hard Seltzer"],
    "CAN White Claw Peach ": ["Hard Seltzer"],
    "CAN White Claw Peach (Fs) ": ["Hard Seltzer"],
    "Can Guinness": ["Cans / Prem Bottle"],
    "Can Heineken Zero": ["Cans / Prem Bottle"],
    "Can Twisted Tea": ["Cans / Prem Bottle"],
    "Can White Claw Black Cherry": ["Hard Seltzer"],
    "Can White Claw Black Cherry (Fs)": ["Hard Seltzer"],
    "Can White Claw Mango": ["Hard Seltzer"],
    "Can White Claw Mango (Fs)": ["Hard Seltzer"],
    "Can White Claw Peach": ["Hard Seltzer"],
    "Can White Claw Peach (Fs)": ["Hard Seltzer"],
    "Dos Xx Lager Bottle": ["Prem Bottle", "Mexi Bottles"], # Normalized form
    "Truly Pineapple": ["Hard Seltzer"],
    "Truly Pineapple (Fs)": ["Hard Seltzer"],
    # "Truly Wild Berry (Fs)": ["Hard Seltzer"], # Duplicate, already present above
    "Coronita Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    # "Budweiser Bottle": ["Dom Bottle"], # Duplicate
    # "Michelob Ultra Bottle": ["Dom Bottle"], # Duplicate

    # Drafts that didn't categorize
    "805 16Oz": ["Prem Pint"],
    "805 32Oz": ["Prem 32oz"],
    "805 Pitcher": ["Prem Pitcher"],
    "Alaskan Amber 16Oz": ["Prem Pint"],
    "Alaskan Amber 32Oz": ["Prem 32oz"],
    "Blue Moon 16Oz": ["Prem Pint"],
    "Blue Moon 32Oz": ["Prem 32oz"],
    "Bud Light 16Oz": ["Dom Pint"],
    "Bud Light 32Oz": ["Dom 32oz"],
    "Church Music 16Oz": ["Craft Pints"],
    "Church Music 32Oz": ["Craft Pints"],
    "Coors Light 16Oz": ["Dom Pint"],
    "Coors Light 32Oz": ["Dom 32oz"],
    "Dos Xx Lager 16Oz": ["Prem Pint"], # Normalized form
    "Dos Xx Lager 32Oz": ["Prem 32oz"], # Normalized form
    "Dos Xx Lager Pitcher": ["Prem Pitcher"], # Normalized form
    "Juicy Haze 16Oz": ["Prem Pint"],
    "Juicy Haze 32Oz": ["Prem 32oz"],
    "Lagunitas Ipa 16Oz": ["Craft Pints"], # Normalized: Lagunitas Ipa 16Oz
    "Lagunitas Ipa 32Oz": ["Craft 32oz"], # Normalized: Lagunitas Ipa 32Oz
    "Lagunitas Ipa Pitcher": ["Craft Pints"], # Normalized: Lagunitas Ipa Pitcher
    "Michelob Ultra 16Oz": ["Dom Pint"],
    "Michelob Ultra 32Oz": ["Dom 32oz"],
    "Miller Lite 16Oz": ["Dom Pint"],
    "Miller Lite 32Oz": ["Dom 32oz"],
    "Modelo Especial 16Oz": ["Prem Pint"],
    "Modelo Especial 32Oz": ["Prem 32oz"],
    "Tower Station 16Oz": ["Craft Pints"],
    "Tower Station 32Oz": ["Craft 32oz"],
    "Zipps Lager 16Oz": ["Craft Pints"],
    "Zipps Lager 32Oz": ["Craft 32oz"],
    "Zipps Lager Pitcher": ["Craft Pitcher"],

    # Domestic Draft (some might be redundant due to normalization, keeping for safety)
    "Bud Light 16oz": ["Dom Pint"], # Normalized: Bud Light 16Oz
    "Bud Light 32oz": ["Dom 32oz"], # Normalized: Bud Light 32Oz
    "Bud Light Pitcher": ["Dom Pitcher"],
    "Coors Light 16oz": ["Dom Pint"], # Normalized: Coors Light 16Oz
    "Coors Light 32oz": ["Dom 32oz"], # Normalized: Coors Light 32Oz
    "Coors Light Pitcher": ["Dom Pitcher"],
    "Michelob Ultra 16oz": ["Dom Pint"], # Normalized: Michelob Ultra 16Oz
    "Michelob Ultra 32oz": ["Dom 32oz"], # Normalized: Michelob Ultra 32Oz
    "Michelob Ultra Pitcher": ["Dom Pitcher"],
    "Miller Lite 16oz": ["Dom Pint"], # Normalized: Miller Lite 16Oz
    "Miller Lite 32oz": ["Dom 32oz"], # Normalized: Miller Lite 32Oz
    "Miller Lite Pitcher": ["Dom Pitcher"],

    # Premium Draft
    "Dos XX Lager 16oz": ["Prem Pint"], # Normalized: Dos Xx Lager 16Oz
    "Dos XX Lager 32oz": ["Prem 32oz"], # Normalized: Dos Xx Lager 32Oz
    "Dos XX Lager Pitcher": ["Prem Pitcher"], # Normalized: Dos Xx Lager Pitcher
    "Modelo Especial 16oz": ["Prem Pint"], # Normalized: Modelo Especial 16Oz
    "Modelo Especial 32oz": ["Prem 32oz"], # Normalized: Modelo Especial 32Oz
    "Modelo Especial Pitcher": ["Prem Pitcher"],
    "Blue Moon 16oz": ["Prem Pint"], # Normalized: Blue Moon 16Oz
    "Blue Moon 32oz": ["Prem 32oz"], # Normalized: Blue Moon 32Oz
    "Blue Moon Pitcher": ["Prem Pitcher"],
    "Alaskan Amber 16oz": ["Prem Pint"], # Normalized: Alaskan Amber 16Oz
    "Alaskan Amber 32oz": ["Prem 32oz"], # Normalized: Alaskan Amber 32Oz
    "Alaskan Amber Pitcher": ["Prem Pitcher"],
    "Juicy Haze 16oz": ["Prem Pint"], # Normalized: Juicy Haze 16Oz
    "Juicy Haze 32oz": ["Prem 32oz"], # Normalized: Juicy Haze 32Oz
    "Juicy Haze Pitcher": ["Prem Pitcher"],

    # Craft Draft
    "Church Music 16oz": ["Craft Pints"], # Normalized: Church Music 16Oz
    "Church Music 32oz": ["Craft Pints"], # Normalized: Church Music 32Oz
    "Church Music Pitcher": ["Craft Pitcher"],
    "Lagunitas IPA 16oz": ["Craft Pints"], # Normalized: Lagunitas Ipa 16Oz
    "Lagunitas IPA 32oz": ["Craft Pints"], # Normalized: Lagunitas Ipa 32Oz
    "Lagunitas IPA Pitcher": ["Craft Pitcher"], # Normalized: Lagunitas Ipa Pitcher
    "Tower Station 16oz": ["Craft Pints"], # Normalized: Tower Station 16Oz
    "Tower Station 32oz": ["Craft Pints"], # Normalized: Tower Station 32Oz
    "Tower Station Pitcher": ["Craft Pitcher"],
    "Zipps Lager 16oz": ["Craft Pints"], # Normalized: Zipps Lager 16Oz
    "Zipps Lager 32oz": ["Craft Pints"], # Normalized: Zipps Lager 32Oz

    # House Wines $5
    "House Cab GL": ["House Wines"], # Normalized: House Cab Gl
    "House Cab Gl": ["House Wines"],
    "House Chard GL": ["House Wines"], # Normalized: House Chard Gl
    "House Chard Gl": ["House Wines"],
    "House White Zin GL": ["House Wines"], # Normalized: House White Zin Gl
    "House Merlot GL": ["House Wines"], # Normalized: House Merlot Gl
    "House Merlot Gl": ["House Wines"],
    "House White Zin Gl": ["House Wines"],

    # Premium Wines
    "20 Acres Cab GL": ["Prem Wines"], # Normalized: 20 Acres Cab Gl
    "Champagne GL": ["Prem Wines"], # Normalized: Champagne Gl
    "Infamous Goose Sauv Blanc GL": ["Prem Wines"], # Normalized: Infamous Goose Sauv Blanc Gl
    "Kendall Jackson Chard GL": ["Prem Wines"], # Normalized: Kendall Jackson Chard Gl
    "La Crema Chard GL": ["Prem Wines"], # Normalized: La Crema Chard Gl
    "La Crema Pinot Noir GL": ["Prem Wines"], # Normalized: La Crema Pinot Noir Gl
    "La Marca Prosecco GL": ["Prem Wines"], # Normalized: La Marca Prosecco Gl
    "Troublemaker Red Blend GL": ["Prem Wines"], # Normalized: Troublemaker Red Blend Gl
    "Villa Sandi Pinot Grigio GL": ["Prem Wines"], # Normalized: Villa Sandi Pinot Grigio Gl

    # Mimosa $5
    "Mimosa": ["Mimosa"],
    "Mimosa Fs": ["Mimosa"],

    #Liquor
    "Old Fashion Bulleit Rye": ["Bulleit Old Fashioned"],
    "Crown Royal (Fs)": ["Crown Royal"],
    "Crown Royal": ["Crown Royal"],
    "Crown Apple (Fs)": ["Crown Royal"],
    "Crown Apple": ["Crown Royal"],
    "Desert Donkey Milagro": ["Desert Donkey Milagro"],
    "Desert Donkey Titos": ["Desert Donkey Tito's"], # Normalized: Desert Donkey Titos
    "Fireball": ["Fireball"],
    "Fireball (Fs)": ["Fireball"],
    "Four Roses Bourbon (Fs)": ["Four Roses"],
    "Four Roses Bourbon": ["Four Roses"],
    "Old Fashion Four Roses": ["Four Roses Old Fashioned"],
    "Green Tea": ["Green Tea"],
    "Hendricks": ["Hendricks"],
    "Hendricks (Fs)": ["Hendricks"],
    "Iceberg": ["Iceberg"],
    "Jack Daniels": ["Jack Daniels"],
    "Jack Daniels (Fs)": ["Jack Daniels"],
    "Jameson": ["Jameson"],
    "Jameson (Fs)": ["Jameson"],
    "Ketel One": ["Ketel One"],
    "Ketel One (Fs)": ["Ketel One"],
    "Milagro Anejo": ["Milagro (Anejo)"],
    "Milagro Silver & Rep": ["Milagro (Silver & Rep)"], # Normalized: Milagro Silver & Rep
    "Titos": ["Tito'S"], # Normalized: Titos
    "Milagro Anejo (Fs)": ["Milagro (Anejo)"],
    "Milagro Silver & Rep (Fs)": ["Milagro (Silver & Rep)"], # Normalized: Milagro Silver & Rep (Fs)
    "Screwball": ["Screwballs"],
    "Screwball (Fs)": ["Screwballs"],
    "Titos (Fs)": ["Tito'S"], # Normalized: Titos (Fs)
    "Titos Bloody": ["Tito's Screw/Bloody"], # Normalized: Titos Bloody
    "Titos Screw": ["Tito's Screw/Bloody"], # Normalized: Titos Screw
    "Well Whiskey": ["Well"],
    "Well Whiskey (Fs)": ["Well"],
    "Well Gin": ["Well"],
    "Well Gin (Fs)": ["Well"],
    "Well Vodka": ["Well"],
    "Well Vodka (Fs)": ["Well"],
    "Well Rum": ["Well"],
    "Well Rum (Fs)": ["Well"],
    "Well Scotch": ["Well"],
    "Well Scotch (Fs)": ["Well"],
    "Double Well": ["Well"],
    "Western Son": ["WS Sons Vodka"],
    "Western Son (Fs)": ["WS Sons Vodka"],
    "Western Son Blueberry": ["WS Sons Vodka"],
    "Western Son Raspberry (Fs)": ["WS Sons Vodka"],
    "Western Son Lemon": ["WS Sons Vodka"],
    "Western Son Lemon (Fs)": ["WS Sons Vodka"],
    "Western Son Prickly Pear": ["WS Sons Vodka"],
    "Western Son Prickly Pear (Fs)": ["WS Sons Vodka"],
    "Western Son Prickly Pear (Bump)": ["WS Sons Vodka"],
    "Western Son Raspberry": ["WS Sons Vodka"],
    "Zipparita": ["Zipparita"],
    "Zipparita Straw": ["Zipparita Flavored"],

    #more (some might be redundant)
    "Jack Fire": ["Jack Daniels"],
    "Jack Fire (Fs)": ["Jack Daniels"],
    "Milagro": ["Milagro (Silver & Rep)"],
    "Milagro (Fs)": ["Milagro (Silver & Rep)"],
    # "Milagro Anejo (Fs)": ["Fireball"], # This was in original, seems like a typo. Keeping previous Milagro Anejo mapping.
    "Milagro Reposado": ["Milagro (Silver & Rep)"],
    "Milagro Reposado (Fs)": ["Milagro (Silver & Rep)"],
    "Well Tequila": ["Well"],
    "Well Tequila (Fs)": ["Well"],
    "20 Acres Cab Gl": ["Prem Wines"], # Normalized form
    "Champagne Gl": ["Prem Wines"], # Normalized form
    # "House Cab Gl": ["House Wines"], # Duplicate
    # "House Chard Gl": ["House Wines"], # Duplicate
    # "House White Zin Gl": ["House Wines"], # Duplicate
    "Infamous Goose Sauv Blanc Gl": ["Prem Wines"], # Normalized form
    "Kendall Jackson Chard Gl": ["Prem Wines"], # Normalized form
    "La Crema Chard Gl": ["Prem Wines"], # Normalized form
    "La Crema Pinot Noir Gl": ["Prem Wines"], # Normalized form
    "La Marca Prosecco Gl": ["Prem Wines"], # Normalized form
    # "Mimosa Fs": ["Mimosa"], # Duplicate
    "Troublemaker Red Blend Gl": ["Prem Wines"], # Normalized form
    "Villa Sandi Pinot Grigio Gl": ["Prem Wines"], # Normalized form

    # Items from the unmapped list in the previous output (many are already covered or will be by normalization)
    "1000 Island": ["Other"],
    "Add All White": ["Add Ons"],
    "Add Bacon": ["Add Ons"],
    "Add Black Beans (Nachos)": ["Add Ons"],
    "Add Black Olives": ["Add Ons"],
    "Add Black Olives (Nachos)": ["Add Ons"],
    "Add Cheddar": ["Add Ons"],
    "Add Cheese (Soups)": ["Add Ons"],
    "Add Corn (Zipps Nachos)": ["Add Ons"],
    "Add Golden Sauce": ["Add Ons"],
    "Add Jalp": ["Add Ons"],
    "Add Jalp (Zipps Nachos)": ["Add Ons"],
    "Add Lettuce": ["Add Ons"],
    "Add Mozzarella": ["Add Ons"],
    "Add Onions (Soups)": ["Add Ons"],
    "Add Pepper Jack": ["Add Ons"],
    "Add Pickled Jalapenos (Nachos)": ["Add Ons"],
    "Add Sauteed Mush": ["Add Ons"],
    "Add Shredded Chicken (Nachos)": ["Add Ons"],
    "Add Sirloin (Nachos)": ["Add Ons"],
    "Add Swiss": ["Add Ons"],
    "Balsamic Vinaigrette": ["Dressings / Sauces"],
    "Blue Cheese": ["Dressings / Sauces"],
    "Caesar": ["Dressings / Sauces"],
    "Extra Hot": ["Wing Sauces"],
    "French Fries (Basket)": ["Baskets"],
    "Honey Balsamic": ["Dressings / Sauces"],
    "Honey Mustard": ["Dressings / Sauces"],
    "Hot": ["Wing Sauces"],
    "Lemon Vinaigrette": ["Dressings / Sauces"],
    "Lt. Olive Vin": ["Dressings / Sauces"], # Normalized: Lt. Olive Vin
    "Medium": ["Wing Sauces"],
    "Mild": ["Wing Sauces"],
    "Oil & Vinegar": ["Dressings / Sauces"], # Normalized: Oil & Vinegar
    "Onion Rings (Basket)": ["Baskets"],
    "Ranch": ["Dressings / Sauces"],
    "Sour Cream Add On": ["Add Ons"],
    "Sweet Jalapeno": ["Dressings / Sauces"], # Normalized: Sweet Jalapeno
    "Sweet Potato Chips (Basket)": ["Baskets"],
    "Toss In Golden": ["Add Ons"],
    "Baskets": ["Baskets"],
    "Buffalo Wings": ["Wings"],
    "Chicken Fingers": ["Chicken Fingers"],
    "Chix Quesadilla": ["Quesadillas"],
    "Golden Wings": ["Wings"],
    "Mozzarella Sticks": ["Appetizers"],
    "Quesadilla": ["Quesadillas"],
    "Sirloin Quesadilla": ["Quesadillas"],
    "1000 Island Burger": ["Burgers"], # Normalized: 1000 Island Burger
    "Bacon Cheeseburger": ["Burgers"],
    "Bbq Bacon Burger": ["Burgers"],
    "Big Zipp Burger": ["Burgers"],
    "Black & Blue Burger": ["Burgers"], # Normalized: Black & Blue Burger
    "Cado Burger": ["Burgers"],
    "Egg It!": ["Burger Add Ons"], # Normalized: Egg It!
    "Green Chili Burger": ["Burgers"],
    "Mushroom Swiss Burger": ["Burgers"],
    "No Onions (Burger)": ["Burger Modifications"],
    "No Pickles": ["Burger Modifications"],
    "Peanut Butter Burger": ["Burgers"],
    "Sweet Jalapeno Burger": ["Burgers"], # Normalized: Sweet Jalapeno Burger
    "Turkey Burger": ["Burgers"],
    "Turkey Patty": ["Burger Modifications"],
    "Veggie Burger": ["Burgers"],
    "Veggie Patty": ["Burger Modifications"],
    "Zipps Burger": ["Burgers"],
    "Classic Root Beer Float": ["Desserts"],
    "Scoop Of Vanilla 1": ["Add Ons"],
    "Scoop Of Vanilla 2": ["Add Ons"],
    "Jimmy It!": ["Focaccia Modifications"], # Normalized: Jimmy It!
    "Scorch Focaccia": ["Focaccia"],
    "Steak Philly Focaccia": ["Focaccia"],
    "Tenderloin Focaccia": ["Focaccia"],
    "Carrots And Ranch": ["Sides"],
    "Kids 2 Slices Of Cheese Pizza": ["Kids Menu"],
    "Kids Carrots And Ranch": ["Kids Menu"],
    "Kids Chicken Fingers": ["Kids Menu"],
    "Kids Chicken Skewers": ["Kids Menu"],
    "Kids Grilled Cheese": ["Kids Menu"],
    "Kids Quesadilla": ["Kids Menu"],
    "Kids Zipps Burger": ["Kids Menu"],
    "Kids Zipps Cheese Burger": ["Kids Menu"],
    "Arnold Palmer": ["Non-Alcoholic Beverages"],
    "Coke": ["Non-Alcoholic Beverages"],
    "Coke Mixer": ["Mixers"],
    "Coke Zero": ["Non-Alcoholic Beverages"],
    "Cranberry Juice Mixer": ["Mixers"],
    "Diet Coke": ["Non-Alcoholic Beverages"],
    "Diet Coke Mixer": ["Mixers"],
    "Iced Tea": ["Non-Alcoholic Beverages"],
    "Kids Lemonade": ["Kids Menu"],
    "Kids Milk": ["Kids Menu"],
    "Kids Mr. Pibb": ["Kids Menu"], # Normalized: Kids Mr. Pibb
    "Kids Root Beer": ["Kids Menu"],
    "Lemonade": ["Non-Alcoholic Beverages"],
    "Mr. Pibb": ["Non-Alcoholic Beverages"], # Normalized: Mr. Pibb
    "Red Bull Mixer": ["Mixers"],
    "Root Beer": ["Non-Alcoholic Beverages"],
    "Sf Red Bull": ["Non-Alcoholic Beverages"],
    "Soda Mixer": ["Mixers"],
    "Soda Water": ["Mixers"],
    "Sprite": ["Non-Alcoholic Beverages"],
    "Sprite Mixer": ["Mixers"],
    "Straw Lemonade": ["Non-Alcoholic Beverages"],
    "Tonic Mixer": ["Mixers"],
    "Zipps Water": ["Non-Alcoholic Beverages"],
    "Beef Sirloin Taco": ["Tacos"],
    "Chicken Taco": ["Tacos"],
    "Fish And Chips": ["Fish Entrees"], # Normalized: Fish And Chips
    "Buffalo Chicken Salad": ["Salads"],
    "Caesar Salad": ["Salads"],
    "Chicken Caesar Salad": ["Salads"],
    "Chicken Greek Salad": ["Salads"],
    "Fried Chicken Salad": ["Salads"],
    "Honey Balsamic Salad": ["Salads"],
    "House Salad": ["Salads"],
    "Side Salad (Zipps)": ["Sides"],
    "Sirloin Taco Salad": ["Salads"],
    "Zipps Chop Salad": ["Salads"],
    "B.L.T. On Sdb": ["Sandwiches"], # Normalized: B.L.T. On Sdb
    "Bbq Chicken Sandwich": ["Sandwiches"],
    "Chicken Club Sandwich": ["Sandwiches"],
    "Club Sandwich": ["Sandwiches"],
    "Southwest Chicken Sandwich": ["Sandwiches"],
    "Spicy Chix Sandwich": ["Sandwiches"],
    "Turkey Sandwich": ["Sandwiches"],
    "1/2 Fries 1/2 Chips": ["Sides"], # Normalized: 1/2 Fries 1/2 Chips
    "1/2 Fries 1/2 Onion Rings": ["Sides"], # Normalized: 1/2 Fries 1/2 Onion Rings
    "1/2 Onion Rings 1/2 Chips": ["Sides"], # Normalized: 1/2 Onion Rings 1/2 Chips
    "Bbq Sauce": ["Dressings / Sauces"],
    "Bulk Dressing": ["Dressings / Sauces"],
    "Chip Refill": ["Add Ons"],
    "Extra Dressing": ["Add Ons"],
    "French Fries": ["Sides"],
    "Kids French Fries": ["Kids Menu"],
    "Onion Rings": ["Sides"],
    "Salsa Refill": ["Add Ons"],
    "Side Bbq Sauce": ["Dressings / Sauces"],
    "Side Beer Cheese": ["Dressings / Sauces"],
    "Side Buffalo Sauce": ["Dressings / Sauces"],
    "Side Chipotle Mayo": ["Dressings / Sauces"],
    "Side Golden Sauce": ["Dressings / Sauces"],
    "Side Jalapenos": ["Add Ons"], # Normalized: Side Jalapenos
    "Side Mayo": ["Dressings / Sauces"],
    "Side Pickle Chips": ["Add Ons"],
    "Side Pico De Gallo": ["Add Ons"], # Normalized: Side Pico De Gallo
    "Side Salad": ["Sides"],
    "Side Sour Cream": ["Add Ons"],
    "Sweet Potato Chips": ["Sides"],
    "Green Bay Chili Bowl": ["Soups / Chili"],
    "S.O.D. Bowl": ["Soups / Chili"], # Normalized: S.O.D. Bowl
    "S.O.D. Cup": ["Soups / Chili"], # Normalized: S.O.D. Cup
    "Sub Carrots & Celery": ["Substitutions"], # Normalized: Sub Carrots & Celery
    "Sub Casear Salad": ["Substitutions"], # Normalized: Sub Casear Salad
    "Sub Pepper Jack": ["Substitutions"],
    "Sub Provolone": ["Substitutions"],
    "Sub Turkey Patty": ["Substitutions"],
    "Ground Beef Topping (Slice)": ["Pizza Toppings"],
    "Pepperoni Topping (Slice)": ["Pizza Toppings"],
    "Sausage Topping (Slice)": ["Pizza Toppings"],
    "Slice Of Pizza": ["Pizza Slices"],
    # "Iceberg": ["Iceberg"], # Duplicate
    "Makers Mark": ["Makers Mark"],
    "Kahlua (Fs)": ["Kahlua"],
    "Big Zipparita": ["Zipparita"],
    "Bloody Mary": ["Bloody Mary"],
    "Chambord Flavor": ["Flavor Shots"],
    "Chambord Flavor 24Oz To Go": ["Flavor Shots"], # Normalized: Chambord Flavor 24Oz To Go
    "Espresso Martini": ["Martinis"],
    "Firecracker Flavor": ["Flavor Shots"],
    "Firecracker Flavor 24Oz To Go": ["Flavor Shots"], # Normalized: Firecracker Flavor 24Oz To Go
    "Gran Mar Flavor": ["Flavor Shots"],
    "Gran Mar Flavor 24Oz To Go": ["Flavor Shots"], # Normalized: Gran Mar Flavor 24Oz To Go
    "Gran Mar Flavor Big Rita": ["Flavor Shots"],
    "Grateful Flavor": ["Flavor Shots"],
    "Mango Flavor": ["Flavor Shots"],
    "Melon Flavor": ["Flavor Shots"],
    "Milagro Anejo Flavor": ["Flavor Shots"],
    "Milagro Margarita": ["Milagro Margarita"],
    "Milagro Silver Flavor": ["Flavor Shots"],
    "Moscow Mule Titos": ["Moscow Mules"], # Normalized: Moscow Mule Titos
    "Peach Flavor": ["Flavor Shots"],
    "Strawberry Flavor": ["Flavor Shots"],
    # "Titos Bloody": ["Tito's Screw/Bloody"], # Duplicate
    "To Go Rita 24Oz": ["To Go Drinks"], # Normalized: To Go Rita 24Oz
    "Watermelon Flavor": ["Flavor Shots"],
    "White Tea": ["White Tea"],
    # "Zippa Rona": ["Zipparona"], # Duplicate
    # "Zipparita": ["Zipparita"], # Duplicate
    # "Zipparita Straw": ["Zipparita Flavored"], # Duplicate
    "Captain Morgan": ["Captain Morgan"],
    "Patron Silver": ["Patron Silver"],
    "Ketel One (Bump)": ["Ketel One"],
    "Martini Up": ["Martinis"],
    "Cranberry Back": ["Mixers"],
    "Western Son Blueberry (Fs)": ["WS Sons Vodka"],
    # "Western Son Lemon (Fs)": ["WS Sons Vodka"], # Duplicate
    "House Wine": ["House Wines"],
    "Premium Wine": ["Prem Wines"],

    "Beer Cheese Pretzels":["Beer Cheese"],
    "Chicken Rolls":["Chicken Rolls"],
    "Chicken Skewers":["Chicken Skewers"],
    "Chips, Salsa & Guac":["Chips, Salsa & Guac"], # Normalized: Chips, Salsa & Guac
    "Corn Dog Basket":["Corn Dogs"],
    "Nachos (Zipps)":["Nachos"],
    "Philly Steak Rolls":["Philly Rolls"],
    "Brownie Skillet":["Dessert Skillets"],
    "Choc Chip Cookie Skillet":["Dessert Skillets"],
    "White Choc Cookie Skillet":["Dessert Skillets"],
    "Zippapillas": ["Zippapillas"],
    "Buffalo Focaccia":["Focaccia - (All Other Chicken)"],
    "Chicken Caesar Focaccia":["Focaccia - (All Other Chicken)"],
    "Chicken Focaccia":["Focaccia - Chicken, Club"],
    "Chicken Philly Focaccia":["Focaccia - (All Other Chicken)"],
    "Club Focaccia":["Focaccia - Chicken, Club"],
    "Golden Focaccia":["Focaccia - (All Other Chicken)"],
    "Monaco Focaccia":["Focaccia - (All Other Chicken)"],
    "Pepper Jack Focaccia":["Focaccia - (All Other Chicken)"],
    "Scorch Focaccia:":["Focaccia - (All Other Chicken)"], # Normalized: Scorch Focaccia:
    "Chicken Burrito":["Burritos (All)"],
    # "Fish and Chips":["Fish Entrees (All)"], # Ambiguity: "Fish And Chips" maps to "Fish Entrees", here to "Fish Entrees (All)"
    "Fish Taco":["Tacos-Fish"],
    "Sirloin Burrito":["Burritos (All)"],
    "Tacos":["Tacos - Chicken/Sirloin"],
    "Zipps Dog":["Zipps Dog"],
    # "Slice Of Pizza":["Pizza Slices"], # Duplicate
    "Fish And Chips ":["Fish Entrees (All)"], # Note: Trailing space, will be normalized
    '18" Pizza Pie':['Pizza 18" Whole'], # Normalized: 18" Pizza Pie
    '18" Pizza Pie ':['Pizza 18" Whole'], # Note: Trailing space
}


key_to_sheet_label = {
    "Dom Bottle $4.50": "Dom Bottle $4.50",
    "Dom Bottle $5.00": "Dom Bottle $5", # Key will be "Dom Bottle $5" after formatting
    "Dom Bottle $5": "Dom Bottle $5",
    "Cans / Prem Bottle $5.00": "Cans / Prem Bottle $5", # Key will be "Cans / Prem Bottle $5"
    "Cans / Prem Bottle $5": "Cans / Prem Bottle $5",
    "Mexi Bottles $5.50": "Mexi Bottles $5.50",
    "Hard Seltzers $5.00": "Hard Seltzers $5", # Key will be "Hard Seltzers $5"
    "Hard Seltzers $5": "Hard Seltzers $5",
    "Hard Seltzers $5.50": "Hard Seltzers $5.50",
    "Hard Seltzer $5.00": "Hard Seltzer $5",
    "Hard Seltzer $5": "Hard Seltzer $5",
    "Hard Seltzer $5.50": "Hard Seltzer $5.50",
    "Dom Bucket $23.00": "Dom Bucket $23", # Key will be "Dom Bucket $23"
    "Dom Bucket $23": "Dom Bucket $23",
    "Coronita Bucket $24 $24": "Coronita Bucket $24", # Price part seems unusual in key "Coronita Bucket $24 $24"
    "Zipparona $14.00": "Zipparona $14", # Key will be "Zipparona $14"
    "Zipparona $14": "Zipparona $14",

    "Dom Pint $5.00": "Dom Pint $5", # Key will be "Dom Pint $5"
    "Dom Pint $5": "Dom Pint $5",
    "Dom 32oz $7.00": "Dom 32oz $7", # Key will be "Dom 32oz $7"
    "Dom 32oz $7": "Dom 32oz $7",
    "Prem Pint $5.00": "Prem Pint $5", # Key will be "Prem Pint $5"
    "Prem Pint $5": "Prem Pint $5",
    "Prem Pint $5.50": "Prem Pint $5.50",
    "Craft Pints $5.00": "Craft Pints $5", # Key will be "Craft Pints $5"
    "Craft Pints $5": "Craft Pints $5",
    "Craft Pints $5.50": "Craft Pints $5.50",
    "Prem Pitcher $14.00": "Prem Pitcher $14", # Key will be "Prem Pitcher $14"
    "Prem Pitcher $14": "Prem Pitcher $14",

    "House Wines $5.00": "House Wines $5", # Key will be "House Wines $5"
    "House Wines $5": "House Wines $5",
    "Prem Wines $7.00": "Prem Wines $7", # Key will be "Prem Wines $7"
    "Prem Wines $7": "Prem Wines $7",
    "Prem Wines $8.00": "Prem Wines $8", # Key will be "Prem Wines $8"
    "Prem Wines $8": "Prem Wines $8",
    "Mimosa $5.00": "Mimosa $5", # Key will be "Mimosa $5"
    "Mimosa $5": "Mimosa $5",

    "Bulleit Old Fashioned $8.00": "Bulleit Old Fashioned $8",
    "Bulleit Old Fashioned $8": "Bulleit Old Fashioned $8",
    "Crown Royal $6.50": "Crown Royal $6.50",
    "Desert Donkey Milagro $7.50": "Desert Donkey Milagro $7.50",
    "Desert Donkey Tito's $7.50": "Desert Donkey Tito's $7.50",
    "Fireball $4.00": "Fireball $4", # Key will be "Fireball $4"
    "Fireball $4": "Fireball $4",
    "Four Roses $5.00": "Four Roses $5", # Key will be "Four Roses $5"
    "Four Roses $5": "Four Roses $5",
    "Four Roses $5.50": "Four Roses $5.50",
    "Four Roses Old Fashioned $8.00": "Four Roses Old Fashioned $8",
    "Four Roses Old Fashioned $8": "Four Roses Old Fashioned $8",
    "Green Tea $5.00": "Green Tea $5", # Key will be "Green Tea $5"
    "Green Tea $5": "Green Tea $5",
    "Hendricks $6.50": "Hendricks $6.50",
    "Iceberg $0.75": "Iceberg $0.75",
    "Jack Daniels $5.00": "Jack Daniels $5", # Key will be "Jack Daniels $5"
    "Jack Daniels $5": "Jack Daniels $5",
    "Jack Daniels $5.50": "Jack Daniels $5.50",
    "Jack Daniels $6.50": "Jack Daniels $6.50",
    "Jameson $5.00": "Jameson $5", # Key will be "Jameson $5"
    "Jameson $5": "Jameson $5",
    "Jameson $5.50": "Jameson $5.50",
    "Jameson $6.50": "Jameson $6.50",
    "Ketel One $5.00": "Ketel One $5", # Key will be "Ketel One $5"
    "Ketel One $5": "Ketel One $5",
    "Ketel One $6.50": "Ketel One $6.50",
    "Milagro (Anejo) $5.00": "Milagro (Anejo) $5",
    "Milagro (Anejo) $5": "Milagro (Anejo) $5",
    "Milagro (Anejo) $5.50": "Milagro (Anejo) $5.50",
    "Milagro (Anejo) $6.50": "Milagro (Anejo) $6.50",
    "Milagro (Silver & Rep) $5.00": "Milagro (Silver & Rep) $5",
    "Milagro (Silver & Rep) $5.0": "Milagro (Silver & Rep) $5", # Redundant due to formatting
    "Milagro (Silver & Rep) $5": "Milagro (Silver & Rep) $5",
    "Milagro (Silver & Rep) $5.50": "Milagro (Silver & Rep) $5.50",
    "Milagro (Silver & Rep) $6.50": "Milagro (Silver & Rep) $6.50",
    "Screwballs $4.00": "Screwballs $4",
    "Screwballs $4": "Screwballs $4",
    "Tito'S $5.50": "Tito'S $5.50",
    "Tito'S $6.50": "Tito'S $6.50",
    "Tito's Screw/Bloody $6.50": "Tito's Screw/Bloody $6.50",
    "Well $4.25": "Well $4.25",
    "WS Sons Vodka $4.00": "WS Sons Vodka $4",
    "WS Sons Vodka $4": "WS Sons Vodka $4",
    "Zipparita $5.00": "Zipparita $5",
    "Zipparita $5.0": "Zipparita $5", # Redundant
    "Zipparita $5": "Zipparita $5",
    "Zipparita $5.50": "Zipparita $5.50",
    "Zipparita Flavored $6.25": "Zipparita Flavored $6.25",
    "Zipparita Flavored $6.75": "Zipparita Flavored $6.75",

    "Beer Cheese $7.00":"Beer Cheese $7",
    "Beer Cheese $7":"Beer Cheese $7",
    "Beer Cheese $8.00":"Beer Cheese $8",
    "Beer Cheese $8":"Beer Cheese $8",
    "Burritos (All) $7.00":"Burritos (All) $7",
    "Burritos (All) $7":"Burritos (All) $7",
    "Chicken Rolls $7.00":"Chicken Rolls $7",
    "Chicken Rolls $7":"Chicken Rolls $7",
    "Chicken Skewers $12.00":"Chicken Skewers $12",
    "Chicken Skewers $12":"Chicken Skewers $12",
    "Chips, Salsa & Guac $5.50":"Chips, Salsa, & Guac $5.50", # Original had "& Guac" vs "Guac"
    "Chips, Salsa, & Guac $5.50":"Chips, Salsa, & Guac $5.50",
    "Corn Dogs $7.00":"Corn Dogs $7",
    "Corn Dogs $7":"Corn Dogs $7",
    "Dessert Skillets $8.00":"Dessert Skillets $8",
    "Dessert Skillets $8":"Dessert Skillets $8",
    "Fish Entrees (All) $9.00":"Fish Entrees (All) $9",
    "Fish Entrees (All) $9.0": "Fish Entrees (All) $9", # Redundant
    "Fish Entrees (All) $9":"Fish Entrees (All) $9",
    "Focaccia - (All Other Chicken) $12.00":"Focaccia - (All Other Chicken) $12",
    "Focaccia - (All Other Chicken) $12":"Focaccia - (All Other Chicken) $12",
    "Focaccia - Chicken, Club $12.00":"Focaccia - Chicken, Club $12",
    "Focaccia - Chicken, Club $12":"Focaccia - Chicken, Club $12",
    "Nachos $8.00":"Nachos $8",
    "Nachos $8":"Nachos $8",
    "Philly Rolls $7.00":"Philly Rolls $7",
    "Philly Rolls $7":"Philly Rolls $7",
    "Pizza Slices $3.25":"Pizza Slices $3.25",
    'Pizza 18" Whole $16.00':'Pizza 18" Whole $16',
    'Pizza 18" Whole $16':'Pizza 18" Whole $16',
    "Tacos - Chicken/Sirloin $7.00":"Tacos - Chicken/Sirloin $7",
    "Tacos - Chicken/Sirloin $7":"Tacos - Chicken/Sirloin $7",
    "Tacos - Fish $7.00":"Tacos - Fish $7",
    "Tacos - Fish $7":"Tacos - Fish $7",
    "Tacos-Fish $7.00":"Tacos-Fish $7", # Assuming "Tacos-Fish" is a category
    "Tacos-Fish $7":"Tacos-Fish $7",
    "Zippapillas $7.00":"Zippapillas $7",
    "Zippapillas $7":"Zippapillas $7",
    "Zipps Dog $7.00":"Zipps Dog $7",
    "Zipps Dog $7":"Zipps Dog $7",
    "Fish And Chips $9.00":"Fish Entrees (All) $9", # For category "Fish Entrees (All)"
    "Fish And Chips $9":"Fish Entrees (All) $9",     # For category "Fish Entrees (All)"
}


DESIRED_ORDER_FINAL_CSV = [
    "Dom Bottle $4.50",
    "Dom Bottle $5",
    "Cans / Prem Bottle $5",
    "Mexi Bottles $5.50",
    "Hard Seltzer $5", # Added this line from display order, assuming it's needed
    "Hard Seltzer $5.50", # Added this line from display order
    "Hard Seltzers $5", # Keeping this as it's in the original final_ordered list
    "Hard Seltzers $5.50", # Keeping this
    "Dom Bucket $23",
    "Coronita Bucket $24",
    "Zipparona $14",
    "Dom Pint $5",
    "Dom 32oz $7",
    "Prem Pint $5",
    "Prem Pint $5.50",
    "Craft Pints $5",
    "Craft Pints $5.50",
    "Prem Pitcher $14",
    "House Wines $5",
    "Prem Wines $7",
    "Prem Wines $8",
    "Mimosa $5",
    "Bulleit Old Fashioned $8",
    "Crown Royal $6.50",
    "Desert Donkey Milagro $7.50",
    "Desert Donkey Tito's $7.50",
    "Fireball $4",
    "Four Roses $5",
    "Four Roses $5.50",
    "Four Roses Old Fashioned $8",
    "Green Tea $5",
    "Hendricks $6.50",
    "Iceberg $0.75",
    "Jack Daniels $5",
    "Jack Daniels $5.50",
    "Jack Daniels $6.50",
    "Jameson $5",
    "Jameson $5.50",
    "Jameson $6.50",
    "Ketel One $5",
    "Ketel One $6.50",
    "Milagro (Anejo) $5",
    "Milagro (Anejo) $5.50",
    "Milagro (Anejo) $6.50",
    "Milagro (Silver & Rep) $5",
    "Milagro (Silver & Rep) $5.50",
    "Milagro (Silver & Rep) $6.50",
    "Screwballs $4",
    "Tito'S $5.50",
    "Tito'S $6.50",
    "Tito's Screw/Bloody $6.50",
    "Well $4.25",
    "WS Sons Vodka $4",
    "Zipparita $5",
    "Zipparita $5.50",
    "Zipparita Flavored $6.25",
    "Zipparita Flavored $6.75",
    "Beer Cheese $7",
    "Beer Cheese $8",
    "Burritos (All) $7",
    "Chicken Rolls $7",
    "Chicken Skewers $12",
    "Chips, Salsa, & Guac $5.50",
    "Corn Dogs $7",
    "Dessert Skillets $8",
    "Fish Entrees (All) $9",
    "Focaccia - (All Other Chicken) $12",
    "Focaccia - Chicken, Club $12",
    "Nachos $8",
    "Philly Rolls $7",
    "Pizza Slices $3.25",
    'Pizza 18" Whole $16',
    "Tacos - Chicken/Sirloin $7",
    "Tacos-Fish $7",
    "Zippapillas $7",
    "Zipps Dog $7"
]

DESIRED_ORDER_DISPLAY = [
    "Dom Bottle $4.50",
    "Dom Bottle $5",
    "Cans / Prem Bottle $5",
    "Mexi Bottles $5.50",
    "Hard Seltzer $5",       # This was in display order, not final_ordered list from script.
    "Hard Seltzer $5.50",  # This was in display order, not final_ordered list from script.
    # Note: Original final_ordered had "Hard Seltzers $5" and "Hard Seltzers $5.50"
    # If "Hard Seltzer" and "Hard Seltzers" are distinct categories, they should both be present
    # in DESIRED_ORDER_FINAL_CSV as well if data for them exists.
    # For now, I've added them to DESIRED_ORDER_FINAL_CSV to match display.
    "Dom Bucket $23",
    "Coronita Bucket $24",
    "Zipparona $14",
    None,  # Line break
    "Dom Pint $5",
    "Dom 32oz $7",
    "Prem Pint $5",
    "Prem Pint $5.50",
    "Craft Pints $5",
    "Craft Pints $5.50",
    "Prem Pitcher $14",
    None,  # Line break
    "House Wines $5",
    "Prem Wines $7",
    "Prem Wines $8",
    "Mimosa $5",
    None,  # Line break
    "Bulleit Old Fashioned $8",
    "Crown Royal $6.50",
    "Desert Donkey Milagro $7.50",
    "Desert Donkey Tito's $7.50",
    "Fireball $4",
    "Four Roses $5",
    "Four Roses $5.50",
    "Four Roses Old Fashioned $8",
    "Green Tea $5",
    "Hendricks $6.50",
    "Iceberg $0.75",
    "Jack Daniels $5",
    "Jack Daniels $5.50",
    "Jack Daniels $6.50",
    "Jameson $5",
    "Jameson $5.50",
    "Jameson $6.50",
    "Ketel One $5",
    "Ketel One $6.50",
    "Milagro (Anejo) $5",
    "Milagro (Anejo) $5.50",
    "Milagro (Anejo) $6.50",
    "Milagro (Silver & Rep) $5",
    "Milagro (Silver & Rep) $5.50",
    "Milagro (Silver & Rep) $6.50",
    "Screwballs $4",
    "Tito'S $5.50",
    "Tito'S $6.50",
    "Tito's Screw/Bloody $6.50",
    "Well $4.25",
    "WS Sons Vodka $4",
    "Zipparita $5",
    "Zipparita $5.50",
    "Zipparita Flavored $6.25",
    "Zipparita Flavored $6.75",
    None,  # Line break
    "Beer Cheese $7",
    "Beer Cheese $8",
    "Burritos (All) $7",
    "Chicken Rolls $7",
    "Chicken Skewers $12",
    "Chips, Salsa, & Guac $5.50",
    "Corn Dogs $7",
    "Dessert Skillets $8",
    "Fish Entrees (All) $9",
    "Focaccia - (All Other Chicken) $12",
    "Focaccia - Chicken, Club $12",
    "Nachos $8",
    "Philly Rolls $7",
    "Pizza Slices $3.25",
    'Pizza 18" Whole $16',
    "Tacos - Chicken/Sirloin $7",
    "Tacos-Fish $7",
    "Zippapillas $7",
    "Zipps Dog $7"
]


# --- Processing Function ---
def process_data(input_df):
    df = input_df.rename(columns={input_df.columns[0]: 'Item'}).copy()

    df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Items Sold'] = pd.to_numeric(df['Items Sold'], errors='coerce')
    df = df.dropna(subset=['Items Sold', 'Price'])

    df['Item'] = (
        df['Item']
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )

    agg_dict = {"Items Sold": "sum"}
    if '% Sales' in df.columns: # Make % Sales aggregation optional
        agg_dict['% Sales'] = 'first'
    
    summary = (
        df.groupby(["Item", "Price"], dropna=False) # dropna=False for groupby to include NA keys if any from Price
        .agg(agg_dict)
        .reset_index()
    )
    # Re-check for NaNs in Price after grouping if they were critical, though earlier dropna should handle.
    summary = summary.dropna(subset=['Price'])


    summary["CategoryList"] = summary["Item"].map(item_to_category)
    
    # Optional: Inform about items not in item_to_category
    unmapped_items = summary[summary["CategoryList"].isna()]["Item"].unique()
    if len(unmapped_items) > 0:
        st.info(f"Note: The following items from the CSV were not found in the 'item_to_category' dictionary and were skipped: {', '.join(unmapped_items)}")

    summary = summary.dropna(subset=["CategoryList"])
    summary = summary.explode("CategoryList")

    # In 'item_to_category', values are lists of strings. After explode, 'CategoryList' contains single strings.
    # So, summary["CategoryList_str"] = summary["CategoryList"] is sufficient.
    summary["CategoryList_str"] = summary["CategoryList"].astype(str) 
    
    summary["Key"] = summary["CategoryList_str"] + " $" + summary["Price"].astype(str)
    summary["Key"] = summary["Key"].str.replace(r"\.0$", "", regex=True) # Converts "$5.0" to "$5"
    
    # Ensures two decimal places for prices like $5.5 -> $5.50, but not for $5
    summary["Key"] = summary["Key"].apply(
        lambda x: x if "$" not in x else (
            x + "0" if (("." in x.split('$')[-1]) and (len(x.split('$')[-1].split('.')[-1]) == 1))
            else x
        )
    )
    
    summary["DiscountSheetLabel"] = summary["Key"].map(key_to_sheet_label)

    unmapped_keys = summary[summary["DiscountSheetLabel"].isna()]["Key"].unique()
    if len(unmapped_keys) > 0:
        st.warning("The following generated keys (Category + Price) were not found in 'key_to_sheet_label' dictionary and associated data was dropped:")
        # Display a manageable number of unmapped keys
        display_limit = 10
        if len(unmapped_keys) > display_limit:
            st.write(list(unmapped_keys[:display_limit]) + [f"...and {len(unmapped_keys) - display_limit} more."])
        else:
            st.write(list(unmapped_keys))


    summary = summary.dropna(subset=["DiscountSheetLabel"])

    final_df = (
        summary.groupby("DiscountSheetLabel")["Items Sold"]
        .sum()
        .reset_index()
    )
    # Note: original script had .sort_values("DiscountSheetLabel") here, which is an alphabetical sort.
    # This is overridden by categorical sort later for final_ordered_df.

    # Create final_ordered_df for CSV export
    final_temp_for_ordering = final_df.copy()
    final_temp_for_ordering['DiscountSheetLabel'] = pd.Categorical(
        final_temp_for_ordering['DiscountSheetLabel'],
        categories=DESIRED_ORDER_FINAL_CSV,
        ordered=True
    )
    final_ordered_df = final_temp_for_ordering.sort_values('DiscountSheetLabel').dropna(subset=['DiscountSheetLabel'])

    # Create final_for_display_df for Streamlit display (with breaks)
    # Merges with 'final_df' (which has the summed 'Items Sold' before categorical sorting)
    # to align with the original Colab script's logic.
    final_for_display_df = pd.DataFrame({'DiscountSheetLabel': DESIRED_ORDER_DISPLAY})
    final_for_display_df = final_for_display_df.merge(final_df, on='DiscountSheetLabel', how='left')
    final_for_display_df['Items Sold'] = final_for_display_df['Items Sold'].fillna('')
    final_for_display_df = final_for_display_df[['DiscountSheetLabel', 'Items Sold']] # Ensure column order

    return final_ordered_df, final_for_display_df

# --- Streamlit App UI ---
st.set_page_config(layout="wide") # Use wide layout for better table display
st.title("Sales Mix Data Processor")

uploaded_file = st.file_uploader("Upload your 'SalesMixByPrice.csv' file", type="csv")

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file, header=3)
        st.success("File uploaded successfully! Processing...")

        final_ordered_data, final_display_data = process_data(raw_df)

        st.header("Processed Data (for display)")
        st.info("This table includes blank rows for readability, matching your desired output format.")
        st.dataframe(final_display_data, hide_index=True, use_container_width=True)

        csv_data = final_ordered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Processed Data as CSV",
            data=csv_data,
            file_name='processed_sales_mix_data.csv',
            mime='text/csv',
            help="This CSV contains the ordered data without the blank rows used for display breaks."
        )

    except Exception as e:
        st.error(f"An error occurred during processing: {str(e)}")
        st.exception(e) # Displays the full traceback for debugging
else:
    st.info("Please upload a CSV file to begin processing.")