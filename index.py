import pandas as pd

data = pd.read_csv('D:/capstone/data/nutritions.csv')

def get_food_recommendations(classification, data, num_items_per_category=2):
    # Define nutritional requirements for each classification
    requirements = {
        'severely stunting': {
            'min_calories': 200,
            'min_protein': 15,
            'categories': ['Meat', 'Dairy', 'Vegetables', 'Fruits', 'Grains']
        },
        'stunting': {
            'min_calories': 150,
            'min_protein': 10,
            'categories': ['Meat', 'Dairy', 'Vegetables', 'Fruits', 'Grains']
        },
        'normal': {
            'min_calories': 100,
            'min_protein': 5,
            'categories': ['Meat', 'Dairy', 'Vegetables', 'Fruits', 'Grains']
        },
        'high': {
            'min_calories': 50,
            'min_protein': 3,
            'categories': ['Vegetables', 'Fruits']
        }
    }
    
    if classification.lower() not in requirements:
        return "Invalid classification. Please choose from: severely stunting, stunting, normal, or high."
    
    req = requirements[classification.lower()]
    recommendations = []
    
    # Filter and select foods for each category
    for category in req['categories']:
        category_foods = data[data['Category'] == category]
        
        if classification == 'high':
            filtered_foods = category_foods[category_foods['Calories'] <= 100]
        else:
            filtered_foods = category_foods[
                (category_foods['Calories'] >= req['min_calories']) |
                (category_foods['Protein (g)'] >= req['min_protein'])
            ]
        
        if len(filtered_foods) == 0:
            filtered_foods = category_foods
            
        selected_foods = filtered_foods.sample(
            n=min(num_items_per_category, len(filtered_foods)),
            replace=False
        )
        
        recommendations.extend(selected_foods.to_dict('records'))
    
    return recommendations

def format_recommendation(foods):
    if isinstance(foods, str):  # If it's an error message
        return foods
        
    result = "Recommended Foods:\n"
    for food in foods:
        result += f"\nFood: {food['Food']}"
        result += f"\nCategory: {food['Category']}"
        result += f"\nCalories: {food['Calories']}"
        result += f"\nProtein: {food['Protein (g)']}g"
        result += f"\nVitamins: A({food['Vitamin A (IU)']}IU), C({food['Vitamin C (mg)']}mg), D({food['Vitamin D (IU)']}IU)"
        result += "\n" + "-"*40
    return result

def get_recommendations_from_input():
    while True:
        print("\nAvailable classifications:")
        print("1. Severely Stunting")
        print("2. Stunting")
        print("3. Normal")
        print("4. High")
        
        classification = input("\nEnter your classification: ").lower()
        
        recommendations = get_food_recommendations(classification, data)
        print(format_recommendation(recommendations))
        
        another = input("\nWould you like another recommendation? (yes/no): ").lower()
        if another != 'yes':
            break

if __name__ == "__main__":
    get_recommendations_from_input()