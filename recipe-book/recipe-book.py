# In progress...
# I have transferred the data from the Recipe book excel but I haven't implemented fully. I think I need to extract the data from the csv files.
# I need to have the data in one place so that it can be displayed in a streamlit style choice for the user on the website. This can be acheived without PHP using only static github page.
# https://docs.google.com/spreadsheets/d/1gX5NEcLElnwTblZZzFXDlFL0e82uCUuERpz0F-T4Kew/edit?gid=1474169975#gid=1474169975
import pandas as pd
import glob
import os

# Folder containing your CSV files
folder = "\Jack\recipe-book\recipe"

# Output file
output_file = "\Jack\recipe-book\recipe-book.csv"

# Your required column order
columns = [
    "Recipe Name", "Calories", "Ingredients", "Prep Time", "Cook Time", "Overall Time",
    "Total Cost (£)", "Cost Per Serving (£)", "Equipment", "Protein (g)", "Carbohydrates (g)",
    "Fat (g)", "Saturated Fat (g)", "Polyunsaturated Fat (g)", "Monounsaturated Fat (g)",
    "Trans Fat (g)", "Fibre (g)", "Sugar (g)", "Cholesterol (g)", "Vitamin A (g)",
    "Thiamin (B1) (g)", "Riboflavin (B2) (g)", "Niacin (B3) (g)", "Pantothenic Acid (B5) (g)",
    "Pyridoxine (B6) (g)", "Folate (B9) (g)", "Cobalamin (B12) (g)", "Vitamin C (g)",
    "Vitamin E (g)", "Vitamin K (g)", "Sodium (g)", "Chloride (g)", "Potassium (g)",
    "Calcium (g)", "Phosphorus (g)", "Magnesium (g)", "Sulphur (g)", "Iron (g)", "Zinc (g)",
    "Iodine (g)", "Selenium (g)", "Copper (g)", "Manganese (g)", "Fluoride (g)",
    "Chromium (g)", "Molybdenum (g)"
]

# Find all CSV files
files = glob.glob(os.path.join(folder, "*.csv"))

dfs = []

def format_recipe_name(filename):
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ")
    name = " ".join(name.split()).title()
    return name

def get_value(df, key):
    row = df[df.iloc[:, 0] == key]
    if not row.empty:
        return row.iloc[0, 1]
    return ""

def extract_ingredients(df):
    ingredients = df.iloc[:, 5].dropna()
    ingredients = [str(x).strip() for x in ingredients if str(x).strip() != ""]
    return ", ".join(ingredients)

def extract_equipment(df):
    equipment = df.iloc[:, 3].dropna()
    equipment = [str(x).strip() for x in equipment if str(x).strip() != ""]
    return ", ".join(equipment)

for file in files:
    df = pd.read_csv(file, header=None)

    recipe_name = format_recipe_name(os.path.basename(file))

    calories = get_value(df, "Calories")
    protein = get_value(df, "Protein (g)")
    carbs = get_value(df, "Carbohydrates (g)")
    fat = get_value(df, "Fat (g)")

    total_cost = get_value(df, "Total Cost (£)")
    cost_per_serving = get_value(df, "Cost per serving (£)")

    prep_time = get_value(df, "Prep Time")
    cook_time = get_value(df, "Cook Time")
    overall_time = get_value(df, "Overall Time")

    ingredients = extract_ingredients(df)
    equipment = extract_equipment(df)

    row = {
        "Recipe Name": recipe_name,
        "Calories": calories,
        "Ingredients": ingredients,
        "Prep Time": prep_time,
        "Cook Time": cook_time,
        "Overall Time": overall_time,
        "Total Cost (£)": total_cost,
        "Cost Per Serving (£)": cost_per_serving,
        "Equipment": equipment,
        "Protein (g)": protein,
        "Carbohydrates (g)": carbs,
        "Fat (g)": fat,
        # Add the rest of your nutrient fields here using get_value(...)
    }

    dfs.append(row)

combined = pd.DataFrame(dfs)
combined = combined[columns]  # reorder
combined.to_csv(output_file, index=False)