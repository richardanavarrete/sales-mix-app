import streamlit as st

st.title("Sales Mix Tool")

# File uploader
uploaded_file = st.file_uploader("Choose a file to upload", type=["csv", "xlsx"])

if uploaded_file is not None:
    # You can read the file using pandas, for example
    import pandas as pd
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    st.write("Preview of uploaded data:")
    st.dataframe(df)

# Load the raw data, specifying the header row and using the first column as 'Item'
df_raw = pd.read_csv("SalesMixByPrice.csv", header=3)

# Assign df_raw to df and rename the first column to 'Item'
df = df_raw.rename(columns={df_raw.columns[0]: 'Item'}).copy()

# Clean 'Price' column: remove '$' and convert to numeric
df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Ensure 'Items Sold' is numeric
df['Items Sold'] = pd.to_numeric(df['Items Sold'], errors='coerce')

# Drop rows where 'Items Sold' or 'Price' are NaN after coercion
df = df.dropna(subset=['Items Sold', 'Price'])

# Normalize 'Item' column: strip, collapse spaces, and standardize casing
df['Item'] = (
    df['Item']
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.title() # Standardize casing to Title Case
)

# Clean up leading and trailing whitespace in the 'Item' column
df['Item'] = df['Item'].str.strip()

# @title
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
    "CAN Austin Cider ": ["Cans / Prem Bottle"],
    "College Street Big Blue Van Bottle": ["Cans / Prem Bottle"],
    "Corona N/A Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Corona Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Corona Premier Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Cornonita Bucket (Zipps)": ["Coronita Bucket $24"],
    "Dos XX Lager Bottle ": ["Cans / Prem Bottle", "Mexi Bottles"],
    "CAN Guinness ": ["Cans / Prem Bottle"], # Added mapping with trailing space
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
    "Can White Claw Mango (Fs)": ["Hard Seltzer"], # Added mapping
    "Can White Claw Peach": ["Hard Seltzer"],
    "Can White Claw Peach (Fs)": ["Hard Seltzer"],
    "Dos Xx Lager Bottle": ["Prem Bottle", "Mexi Bottles"],
    "Truly Pineapple": ["Hard Seltzer"],
    "Truly Pineapple (Fs)": ["Hard Seltzer"],
    "Truly Wild Berry (Fs)": ["Hard Seltzer"],
    "Coronita Bottle": ["Cans / Prem Bottle", "Mexi Bottles"], # Added mapping
    "Budweiser Bottle": ["Dom Bottle"], # Added mapping
    "Michelob Ultra Bottle": ["Dom Bottle"], # Added mapping


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
    "Dos Xx Lager 16Oz": ["Prem Pint"],
    "Dos Xx Lager 32Oz": ["Prem 32oz"],
    "Dos Xx Lager Pitcher": ["Prem Pitcher"],
    "Juicy Haze 16Oz": ["Prem Pint"],
    "Juicy Haze 32Oz": ["Prem 32oz"],
    "Lagunitas Ipa 16Oz": ["Craft Pints"],
    "Lagunitas Ipa 32Oz": ["Craft 32oz"],
    "Lagunitas Ipa Pitcher": ["Craft Pints"],
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
    "Zipps Lager Pitcher": ["Craft Pitcher"], # Added mapping for Zipps Lager Pitcher


    # Domestic Draft
    "Bud Light 16oz": ["Dom Pint"],
    "Bud Light 32oz": ["Dom 32oz"],
    "Bud Light Pitcher": ["Dom Pitcher"], # Corrected category
    "Coors Light 16oz": ["Dom Pint"],
    "Coors Light 32oz": ["Dom 32oz"],
    "Coors Light Pitcher": ["Dom Pitcher"], # Corrected category
    "Michelob Ultra 16oz": ["Dom Pint"],
    "Michelob Ultra 32oz": ["Dom 32oz"],
    "Michelob Ultra Pitcher": ["Dom Pitcher"], # Corrected category
    "Miller Lite 16oz": ["Dom Pint"],
    "Miller Lite 32oz": ["Dom 32oz"],
    "Miller Lite Pitcher": ["Dom Pitcher"], # Corrected category

    # Premium Draft
    "Dos XX Lager 16oz": ["Prem Pint"], # Corrected category
    "Dos XX Lager 32oz": ["Prem 32oz"], # Corrected category
    "Dos XX Lager Pitcher": ["Prem Pitcher"],
    "Modelo Especial 16oz": ["Prem Pint"], # Corrected category
    "Modelo Especial 32oz": ["Prem 32oz"], # Corrected category
    "Modelo Especial Pitcher": ["Prem Pitcher"],
    "Blue Moon 16oz": ["Prem Pint"], # Corrected category
    "Blue Moon 32oz": ["Prem 32oz"], # Corrected category
    "Blue Moon Pitcher": ["Prem Pitcher"],
    "Alaskan Amber 16oz": ["Prem Pint"], # Corrected category
    "Alaskan Amber 32oz": ["Prem 32oz"], # Corrected category
    "Alaskan Amber Pitcher": ["Prem Pitcher"],
    "Juicy Haze 16oz": ["Prem Pint"], # Corrected category
    "Juicy Haze 32oz": ["Prem 32oz"], # Corrected category
    "Juicy Haze Pitcher": ["Prem Pitcher"],

    # Craft Draft
    "Church Music 16oz": ["Craft Pints"],
    "Church Music 32oz": ["Craft Pints"],
    "Church Music Pitcher": ["Craft Pitcher"], # Corrected category
    "Lagunitas IPA 16oz": ["Craft Pints"],
    "Lagunitas IPA 32oz": ["Craft Pints"],
    "Lagunitas IPA Pitcher": ["Craft Pitcher"], # Corrected category
    "Tower Station 16oz": ["Craft Pints"],
    "Tower Station 32oz": ["Craft Pints"],
    "Tower Station Pitcher": ["Craft Pitcher"], # Corrected category
    "Zipps Lager 16oz": ["Craft Pints"],
    "Zipps Lager 32oz": ["Craft Pints"],


    # House Wines $5
    "House Cab GL": ["House Wines"],
    "House Cab Gl": ["House Wines"],
    "House Chard GL": ["House Wines"],
    "House Chard Gl": ["House Wines"],
    "House White Zin GL": ["House Wines"],
    "House Merlot GL": ["House Wines"],
    "House Merlot Gl": ["House Wines"],
    "House White Zin Gl": ["House Wines"],

    # Premium Wines $5

    # Premium Wines $7 or $8
    "20 Acres Cab GL": ["Prem Wines"],
    "Champagne GL": ["Prem Wines"],
    "Infamous Goose Sauv Blanc GL": ["Prem Wines"],
    "Kendall Jackson Chard GL": ["Prem Wines"],
    "La Crema Chard GL": ["Prem Wines"],
    "La Crema Pinot Noir GL": ["Prem Wines"],
    "La Marca Prosecco GL": ["Prem Wines"],
    "Troublemaker Red Blend GL": ["Prem Wines"],
    "Villa Sandi Pinot Grigio GL": ["Prem Wines"],

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
    "Desert Donkey Titos": ["Desert Donkey Tito's"],
    "Fireball": ["Fireball"],
    "Fireball (Fs)": ["Fireball"],
    "Four Roses Bourbon (Fs)": ["Four Roses"], # Corrected spelling
    "Four Roses Bourbon": ["Four Roses"], # Corrected spelling
    "Old Fashion Four Roses": ["Four Roses Old Fashioned"], # Corrected spelling
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
    "Milagro Silver & Rep": ["Milagro (Silver & Rep)"],
    "Titos": ["Tito'S"],
    "Milagro Anejo (Fs)": ["Milagro (Anejo)"],
    "Milagro Silver & Rep (Fs)": ["Milagro (Silver & Rep)"],
    "Screwball": ["Screwballs"],
    "Screwball (Fs)": ["Screwballs"],
    "Titos (Fs)": ["Tito'S"],
    "Titos Bloody": ["Tito's Screw/Bloody"],
    "Titos Screw": ["Tito's Screw/Bloody"],
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
    "Zipparita": ["Zipparita"],
    "Zipparita Straw": ["Zipparita Flavored"],

    #more
    "Crown Apple (Fs)": ["Crown Royal"],
    "Crown Royal (Fs)": ["Crown Royal"],
    "Fireball (Fs)": ["Fireball"],
    "Four Roses Bourbon (Fs)": ["Four Roses"],
    "Jack Daniels (Fs)": ["Jack Daniels"],
    "Jack Fire": ["Jack Daniels"],
    "Jack Fire (Fs)": ["Jack Daniels"],
    "Jameson (Fs)": ["Jameson"],
    "Screwball (Fs)": ["Screwballs"],
    "Well Whiskey (Fs)": ["Well"],
    "Hendricks (Fs)": ["Hendricks"],
    "Well Gin (Fs)": ["Well"],
    "Well Rum (Fs)": ["Well"],
    "Milagro": ["Milagro (Silver & Rep)"],
    "Milagro (Fs)": ["Milagro (Silver & Rep)"],
    "Milagro Anejo (Fs)": ["Fireball"], # This seems like an error based on the key, keeping for now but might need correction
    "Milagro Reposado": ["Milagro (Silver & Rep)"],
    "Milagro Reposado (Fs)": ["Milagro (Silver & Rep)"],
    "Well Tequila": ["Well"],
    "Well Tequila (Fs)": ["Well"],
    "Ketel One (Fs)": ["Ketel One"],
    "Titos (Fs)": ["Tito'S"],
    "Well Vodka (Fs)": ["Well"],
    "Western Son (Fs)": ["WS Sons Vodka"],
    "Western Son Lemon (Fs)": ["WS Sons Vodka"],
    "Western Son Raspberry (Fs)": ["WS Sons Vodka"],
    "20 Acres Cab Gl": ["Prem Wines"],
    "Champagne Gl": ["Prem Wines"],
    "House Cab Gl": ["House Wines"],
    "House Chard Gl": ["House Wines"],
    "House White Zin Gl": ["House Wines"],
    "Infamous Goose Sauv Blanc Gl": ["Prem Wines"],
    "Kendall Jackson Chard Gl": ["Prem Wines"],
    "La Crema Chard Gl": ["Prem Wines"],
    "La Crema Pinot Noir Gl": ["Prem Wines"],
    "La Marca Prosecco Gl": ["Prem Wines"],
    "Mimosa Fs": ["Mimosa"],
    "Troublemaker Red Blend Gl": ["Prem Wines"],
    "Villa Sandi Pinot Grigio Gl": ["Prem Wines"],
    "Western Son (Fs)": ["WS Sons Vodka"],

    # Items from the unmapped list in the previous output
    "Budweiser Bottle": ["Dom Bottle"],
    "Can Twisted Tea": ["Cans / Prem Bottle"],
    "Can White Claw Black Cherry": ["Hard Seltzer"],
    "Can White Claw Mango (Fs)": ["Hard Seltzer"],
    "Corona Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Coronita Bottle": ["Cans / Prem Bottle", "Mexi Bottles"],
    "Michelob Ultra Bottle": ["Dom Bottle"],
    "Truly Pineapple (Fs)": ["Hard Seltzer"],
    "Truly Wild Berry": ["Hard Seltzer"],
    "805 16Oz": ["Prem Pint"],
    "Alaskan Amber 16Oz": ["Prem Pint"],
    "Alaskan Amber 32Oz": ["Prem 32oz"],
    "Blue Moon 16Oz": ["Prem Pint"],
    "Blue Moon 32Oz": ["Prem 32oz"],
    "Blue Moon Pitcher": ["Prem Pitcher"],
    "Bud Light 32Oz": ["Dom 32oz"],
    "Church Music 16Oz": ["Craft Pints"],
    "Church Music 32Oz": ["Craft Pints"],
    "Church Music Pitcher": ["Craft Pitcher"],
    "Coors Light 16Oz": ["Dom Pint"],
    "Coors Light 32Oz": ["Dom 32oz"],
    "Coors Light Pitcher": ["Dom Pitcher"],
    "Dos Xx Lager 16Oz": ["Prem Pint"],
    "Dos Xx Lager 32Oz": ["Prem 32oz"],
    "Dos Xx Lager Pitcher": ["Prem Pitcher"],
    "Juicy Haze 16Oz": ["Prem Pint"],
    "Juicy Haze 32Oz": ["Prem 32oz"],
    "Juicy Haze Pitcher": ["Prem Pitcher"],
    "Michelob Ultra 16Oz": ["Dom Pint"],
    "Michelob Ultra 32Oz": ["Dom 32oz"],
    "Miller Lite 16Oz": ["Dom Pint"],
    "Miller Lite 32Oz": ["Dom 32oz"],
    "Miller Lite Pitcher": ["Dom Pitcher"],
    "Modelo Especial 16Oz": ["Prem Pint"],
    "Modelo Especial 32Oz": ["Prem 32oz"],
    "Tower Station 16Oz": ["Craft Pints"],
    "Tower Station 32Oz": ["Craft 32oz"],
    "Zipps Lager 16Oz": ["Craft Pints"],
    "Zipps Lager Pitcher": ["Craft Pitcher"],
    "1000 Island": ["Other"], # Assuming "Other" for miscellaneous items
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
    "Lt. Olive Vin": ["Dressings / Sauces"],
    "Medium": ["Wing Sauces"],
    "Mild": ["Wing Sauces"],
    "Oil & Vinegar": ["Dressings / Sauces"],
    "Onion Rings (Basket)": ["Baskets"],
    "Ranch": ["Dressings / Sauces"],
    "Sour Cream Add On": ["Add Ons"],
    "Sweet Jalapeno": ["Dressings / Sauces"],
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
    "1000 Island Burger": ["Burgers"],
    "Bacon Cheeseburger": ["Burgers"],
    "Bbq Bacon Burger": ["Burgers"],
    "Big Zipp Burger": ["Burgers"],
    "Black & Blue Burger": ["Burgers"],
    "Cado Burger": ["Burgers"],
    "Egg It!": ["Burger Add Ons"],
    "Green Chili Burger": ["Burgers"],
    "Mushroom Swiss Burger": ["Burgers"],
    "No Onions (Burger)": ["Burger Modifications"],
    "No Pickles": ["Burger Modifications"],
    "Peanut Butter Burger": ["Burgers"],
    "Sweet Jalapeno Burger": ["Burgers"],
    "Turkey Burger": ["Burgers"],
    "Turkey Patty": ["Burger Modifications"],
    "Veggie Burger": ["Burgers"],
    "Veggie Patty": ["Burger Modifications"],
    "Zipps Burger": ["Burgers"],
    "Classic Root Beer Float": ["Desserts"],
    "Scoop Of Vanilla 1": ["Add Ons"],
    "Scoop Of Vanilla 2": ["Add Ons"],
    "Jimmy It!": ["Focaccia Modifications"],
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
    "Kids Mr. Pibb": ["Kids Menu"],
    "Kids Root Beer": ["Kids Menu"],
    "Lemonade": ["Non-Alcoholic Beverages"],
    "Mr. Pibb": ["Non-Alcoholic Beverages"],
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
    "Fish And Chips": ["Fish Entrees"],
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
    "B.L.T. On Sdb": ["Sandwiches"],
    "Bbq Chicken Sandwich": ["Sandwiches"],
    "Chicken Club Sandwich": ["Sandwiches"],
    "Club Sandwich": ["Sandwiches"],
    "Southwest Chicken Sandwich": ["Sandwiches"],
    "Spicy Chix Sandwich": ["Sandwiches"],
    "Turkey Sandwich": ["Sandwiches"],
    "1/2 Fries 1/2 Chips": ["Sides"],
    "1/2 Fries 1/2 Onion Rings": ["Sides"],
    "1/2 Onion Rings 1/2 Chips": ["Sides"],
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
    "Side Jalapenos": ["Add Ons"],
    "Side Mayo": ["Dressings / Sauces"],
    "Side Pickle Chips": ["Add Ons"],
    "Side Pico De Gallo": ["Add Ons"],
    "Side Salad": ["Sides"],
    "Side Sour Cream": ["Add Ons"],
    "Sweet Potato Chips": ["Sides"],
    "Green Bay Chili Bowl": ["Soups / Chili"],
    "S.O.D. Bowl": ["Soups / Chili"],
    "S.O.D. Cup": ["Soups / Chili"],
    "Sub Carrots & Celery": ["Substitutions"],
    "Sub Casear Salad": ["Substitutions"],
    "Sub Pepper Jack": ["Substitutions"],
    "Sub Provolone": ["Substitutions"],
    "Sub Turkey Patty": ["Substitutions"],
    "Ground Beef Topping (Slice)": ["Pizza Toppings"],
    "Pepperoni Topping (Slice)": ["Pizza Toppings"],
    "Sausage Topping (Slice)": ["Pizza Toppings"],
    "Slice Of Pizza": ["Pizza Slices"],
    "Iceberg": ["Iceberg"],
    "Crown Apple (Fs)": ["Crown Royal"],
    "Jack Daniels": ["Jack Daniels"],
    "Jameson": ["Jameson"],
    "Makers Mark": ["Makers Mark"],
    "Kahlua (Fs)": ["Kahlua"],
    "Hendricks (Fs)": ["Hendricks"],
    "Well Gin": ["Well"],
    "Big Zipparita": ["Zipparita"],
    "Bloody Mary": ["Bloody Mary"],
    "Chambord Flavor": ["Flavor Shots"],
    "Chambord Flavor 24Oz To Go": ["Flavor Shots"],
    "Desert Donkey Titos": ["Desert Donkey Tito's"],
    "Espresso Martini": ["Martinis"],
    "Firecracker Flavor": ["Flavor Shots"],
    "Firecracker Flavor 24Oz To Go": ["Flavor Shots"],
    "Gran Mar Flavor": ["Flavor Shots"],
    "Gran Mar Flavor 24Oz To Go": ["Flavor Shots"],
    "Gran Mar Flavor Big Rita": ["Flavor Shots"],
    "Grateful Flavor": ["Flavor Shots"],
    "Mango Flavor": ["Flavor Shots"],
    "Melon Flavor": ["Flavor Shots"],
    "Milagro Anejo Flavor": ["Flavor Shots"],
    "Milagro Margarita": ["Milagro Margarita"],
    "Milagro Silver Flavor": ["Flavor Shots"],
    "Moscow Mule Titos": ["Moscow Mules"],
    "Peach Flavor": ["Flavor Shots"],
    "Strawberry Flavor": ["Flavor Shots"],
    "Titos Bloody": ["Tito's Screw/Bloody"],
    "To Go Rita 24Oz": ["To Go Drinks"],
    "Watermelon Flavor": ["Flavor Shots"],
    "White Tea": ["White Tea"],
    "Zippa Rona": ["Zipparona"],
    "Zipparita": ["Zipparita"],
    "Zipparita Straw": ["Zipparita Flavored"],
    "Captain Morgan": ["Captain Morgan"],
    "Well Rum (Fs)": ["Well"],
    "Milagro": ["Milagro (Silver & Rep)"],
    "Patron Silver": ["Patron Silver"],
    "Well Tequila (Fs)": ["Well"],
    "Ketel One (Bump)": ["Ketel One"],
    "Martini Up": ["Martinis"],
    "Titos": ["Tito'S"],
    "Titos (Fs)": ["Tito'S"],
    "Well Vodka": ["Well"],
    "Cranberry Back": ["Mixers"],
    "House White Zin Gl": ["House Wines"],
    "Infamous Goose Sauv Blanc Gl": ["Prem Wines"],
    "La Marca Prosecco Gl": ["Prem Wines"],
    "Mimosa": ["Mimosa"],
    "Western Son Blueberry (Fs)": ["WS Sons Vodka"],
    "Western Son Lemon (Fs)": ["WS Sons Vodka"],
    "House Wine": ["House Wines"],
    "Premium Wine": ["Prem Wines"],

"Beer Cheese Pretzels":["Beer Cheese"],
"Chicken Rolls":["Chicken Rolls"],
"Chicken Skewers":["Chicken Skewers"],
"Chips, Salsa & Guac":["Chips, Salsa & Guac"],
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
"Scorch Focaccia:":["Focaccia - (All Other Chicken)"],
"Chicken Burrito":["Burritos (All)"],
"Fish and Chips":["Fish Entrees (All)"],
"Fish Taco":["Tacos-Fish"],
"Sirloin Burrito":["Burritos (All)"],
"Tacos":["Tacos - Chicken/Sirloin"],
"Zipps Dog":["Zipps Dog"],
"Slice Of Pizza":["Pizza Slices"],
"Beer Cheese Pretzels":["Beer Cheese"],
"Fish And Chips ":["Fish Entrees (All)"],
"Fish And Chips":["Fish Entrees (All)"],
"Scorch Focaccia":["Focaccia - (All Other Chicken)"],
 '18" Pizza Pie':['Pizza 18" Whole'],
 '18" Pizza Pie ':['Pizza 18" Whole'],
}

# @title
key_to_sheet_label = {
    "Dom Bottle $4.50": "Dom Bottle $4.50",
    "Dom Bottle $5.00": "Dom Bottle $5",
    "Cans / Prem Bottle $5.00": "Cans / Prem Bottle $5",
    "Mexi Bottles $5.50": "Mexi Bottles $5.50",
    "Hard Seltzers $5.00": "Hard Seltzers $5",
    "Hard Seltzers $5.50": "Hard Seltzers $5.50",
    "Dom Bucket $23.00": "Dom Bucket $23",
    "Coronita Bucket $24 $24": "Coronita Bucket $24",
    "Zipparona $14.00": "Zipparona $14",

    "Dom Pint $5.00": "Dom Pint $5",
    "Dom 32oz $7.00": "Dom 32oz $7",
    "Prem Pint $5.00": "Prem Pint $5",
    "Prem Pint $5.50": "Prem Pint $5.50",
    "Craft Pints $5": "Craft Pints $5",
    "Craft Pints $5.50": "Craft Pints $5.50",
    "Prem Pitcher $14": "Prem Pitcher $14",

    "House Wines $5": "House Wines $5",
    "Prem Wines $7": "Prem Wines $7",
    "Prem Wines $8": "Prem Wines $8",
    "Mimosa $5": "Mimosa $5",

    "Bulleit Old Fashioned $8": "Bulleit Old Fashioned $8",
    "Crown Royal $6.50": "Crown Royal $6.50",
    "Desert Donkey Milagro $7.50": "Desert Donkey Milagro $7.50",
    "Desert Donkey Tito's $7.50": "Desert Donkey Tito's $7.50",
    "Fireball $4.00": "Fireball $4",
    "Four Roses $5.00": "Four Roses $5",
    "Four Roses $5.50": "Four Roses $5.50",
    "Four Roses Old Fashioned $8.00": "Four Roses Old Fashioned $8",
    "Green Tea $5.00": "Green Tea $5",
    "Hendricks $6.50": "Hendricks $6.50",
    "Iceberg $0.75": "Iceberg $0.75",
    "Jack Daniels $5": "Jack Daniels $5",
    "Jack Daniels $5.50": "Jack Daniels $5.50",
    "Jack Daniels $6.50": "Jack Daniels $6.50",
    "Jameson $5.00": "Jameson $5",
    "Jameson $5.50": "Jameson $5.50",
    "Jameson $6.50": "Jameson $6.50",
    "Ketel One $5.00": "Ketel One $5",
    "Ketel One $6.50": "Ketel One $6.50",
    "Milagro (Anejo) $5.00": "Milagro (Anejo) $5",
    "Milagro (Anejo) $5.50": "Milagro (Anejo) $5.50",
    "Milagro (Anejo) $6.50": "Milagro (Anejo) $6.50",
    "Milagro (Silver & Rep) $5": "Milagro (Silver & Rep) $5",
    "Milagro (Silver & Rep) $5.50": "Milagro (Silver & Rep) $5.50",
    "Milagro (Silver & Rep) $6.50": "Milagro (Silver & Rep) $6.50",
    "Screwballs $4.00": "Screwballs $4",
    "Tito'S $5.50": "Tito'S $5.50",
    "Tito'S $6.50": "Tito'S $6.50",
    "Tito's Screw/Bloody $6.50": "Tito's Screw/Bloody $6.50",
    "Well $4.25": "Well $4.25",
    "WS Sons Vodka $4": "WS Sons Vodka $4",
    "Zipparita $5.00": "Zipparita $5", # Added mapping for $5 Zipparitas
    "Zipparita $5.50": "Zipparita $5.50",
    "Zipparita Flavored $6.25": "Zipparita Flavored $6.25",
    "Zipparita Flavored $6.75": "Zipparita Flavored $6.75",
    "Cans / Prem Bottle $5": "Cans / Prem Bottle $5",
    "Craft Pints $5": "Craft Pints $5",
    "Dom Bottle $5": "Dom Bottle $5",
    "Fireball $4": "Fireball $4",
    "Four Roses $5": "Four Roses $5",
    "Four Roses Old Fashioned $8": "Four Roses Old Fashioned $8",
    "Green Tea $5": "Green Tea $5",
    "Hard Seltzer $5": "Hard Seltzer $5",
    "Hard Seltzer $5.50": "Hard Seltzer $5.50",
    "House Wines $5": "House Wines $5",
    "Dom Pint $5": "Dom Pint $5",
    "Jack Daniels $5.50": "Jack Daniels $5.50",
    "Ketel One $5": "Ketel One $5",
    "Jameson $5": "Jameson $5",
    "Milagro (Silver & Rep) $5.0": "Milagro (Silver & Rep) $5",
    "Zipparona $14": "Zipparona $14",
    "Prem Pint $5": "Prem Pint $5",
    "Prem Pitcher $14": "Prem Pitcher $14",
    "WS Sons Vodka $4": "WS Sons Vodka $4",
    "Zipparita $5": "Zipparita $5", # Added mapping for $5 Zipparitas (simplified key format)
    "Zipparita $5.0": "Zipparita $5", # Added mapping for $5 Zipparitas (with .0)
    "Dom 32oz $7": "Dom 32oz $7",
    "Dom 32oz $7.0": "Dom 32oz $7",
    "Beer Cheese $7":"Beer Cheese $7",
"Beer Cheese $8":"Beer Cheese $8",
"Burritos (All) $7":"Burritos (All) $7",
"Chicken Rolls $7":"Chicken Rolls $7",
"Chicken Skewers $12":"Chicken Skewers $12",
"Chips, Salsa & Guac $5.50":"Chips, Salsa, & Guac $5.50",
"Corn Dogs $7":"Corn Dogs $7",
"Dessert Skillets $8":"Dessert Skillets $8",
"Fish Entrees (All) $9":"Fish Entrees (All) $9",
"Focaccia - (All Other Chicken) $12":"Focaccia - (All Other Chicken) $12",
"Focaccia - Chicken, Club $12":"Focaccia - Chicken, Club $12",
"Nachos $8":"Nachos $8",
"Philly Rolls $7":"Philly Rolls $7",
"Pizza Slices $3.25":"Pizza Slices $3.25",
'Pizza 18" Whole $16':'Pizza 18" Whole $16',
"Tacos - Chicken/Sirloin $7":"Tacos - Chicken/Sirloin $7",
"Tacos - Fish $7":"Tacos - Fish $7",
"Zippapillas $7":"Zippapillas $7",
"Zipps Dog $7":"Zipps Dog $7",
"Chips, Salsa, & Guac $5.50":"Chips, Salsa, & Guac $5.50",
"Corn Dogs $7":"Corn Dogs $7",
"Dessert Skillets $8":"Dessert Skillets $8",
"Fish Entrees (All) $9":"Fish Entrees (All) $9",
"Tacos-Fish $7":"Tacos-Fish $7",
"Fish And Chips $9":"Fish Entrees (All) $9",
"Fish Entrees (All) $9":"Fish Entrees (All) $9",
"Fish Entrees (All) $9.0": "Fish Entrees (All) $9", # Added the missing mapping
"Fish Entrees (All) $9": "Fish Entrees (All) $9",

}

# @title
# Group by 'Item' and 'Price' to create the 'summary' DataFrame
summary = (
    df.groupby(["Item", "Price"])
    .agg({"Items Sold": "sum", "% Sales": "first"})
    .reset_index()
)

# Apply the item_to_category mapping
summary["CategoryList"] = summary["Item"].map(item_to_category)

# Drop rows where 'CategoryList' is NaN (items not found in the mapping)
summary = summary.dropna(subset=["CategoryList"])

# Explode the 'CategoryList' to have one row per category per item
summary = summary.explode("CategoryList")

# Create the 'Key' column using 'Price' (which likely contains string values from grouping)
# Ensure "Price" in the Key is string and correctly formatted for matching (assuming "X.XX" format is desired)
# Remove trailing '.0' for whole numbers and ensure two decimal places otherwise

# Fix: Ensure CategoryList is a single string before creating the Key
summary["CategoryList_str"] = summary["CategoryList"].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)


summary["Key"] = summary["CategoryList_str"].astype(str) + " $" + summary["Price"].astype(str)

summary["Key"] = summary["Key"].str.replace(r"\.0$", "", regex=True)
summary["Key"] = summary["Key"].apply(lambda x: x if "$" not in x else (x + "0" if "." in x and len(x.split('$')[-1].split('.')[-1]) == 1 else x))


summary["DiscountSheetLabel"] = summary["Key"].map(key_to_sheet_label)

# Find keys that were not mapped
unmapped_keys = summary[summary["DiscountSheetLabel"].isna()]["Key"].unique()
print("\nKeys in 'summary' not found in 'key_to_sheet_label':")
print(unmapped_keys)

summary = summary.dropna(subset=["DiscountSheetLabel"])


final = (
    summary.groupby("DiscountSheetLabel")["Items Sold"]
    .sum()
    .reset_index()
    .sort_values("DiscountSheetLabel")
)

desired_order = [
    "Dom Bottle $4.50",
    "Dom Bottle $5",
    "Cans / Prem Bottle $5",
    "Mexi Bottles $5.50",
    "Hard Seltzer $5",
    "Hard Seltzer $5.50",
    "Hard Seltzers $5",
    "Hard Seltzers $5.50",
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

# Convert the 'DiscountSheetLabel' column to a categorical type with the desired order
final['DiscountSheetLabel'] = pd.Categorical(final['DiscountSheetLabel'], categories=desired_order, ordered=True)

# Sort the DataFrame based on the categorical order
final_ordered = final.sort_values('DiscountSheetLabel')

print("\nFinal DataFrame (Ordered):")
display(final_ordered)


desired_order = [
    "Dom Bottle $4.50",
    "Dom Bottle $5",
    "Cans / Prem Bottle $5",
    "Mexi Bottles $5.50",
    "Hard Seltzer $5",
    "Hard Seltzer $5.50",
    "Dom Bucket $23",
      "Coronita Bucket $24",
    "Zipparona $14",
    None,  # Added line break
    "Dom Pint $5",
    "Dom 32oz $7",
    "Prem Pint $5",
    "Prem Pint $5.50",
    "Craft Pints $5",
    "Craft Pints $5.50",
    "Prem Pitcher $14",
    None,  # Added line break
    "House Wines $5",
    "Prem Wines $7",
    "Prem Wines $8",
    "Mimosa $5",
    None,  # Added line break
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
    None,  # Added line break
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

# Create a new DataFrame from the desired_order list
final_with_breaks = pd.DataFrame({'DiscountSheetLabel': desired_order})

# Merge with the original final DataFrame
final_with_breaks = final_with_breaks.merge(final, on='DiscountSheetLabel', how='left')

# Fill NaN values (for the blank rows) with empty strings for cleaner display
final_with_breaks['Items Sold'] = final_with_breaks['Items Sold'].fillna('')

print("\nFinal DataFrame (Ordered with Breaks):")
display(final_with_breaks)

# New Section


    # --- Display + Download ---
st.subheader("Results")
st.dataframe(final, use_container_width=True)

csv = final.to_csv(index=False).encode("utf-8")
st.download_button("Download Categorized CSV", data=csv, file_name="sales_mix_summary.csv", mime="text/csv")
