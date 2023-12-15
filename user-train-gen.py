import pandas as pd
import random
import uuid

# Parameters for data generation
num_users = 50  # Number of users to generate
health_goals = ['Weight Loss', 'Muscle Gain', 'Maintain Health']  # Health goal options
min_budget, max_budget = 150, 500  # Budget range (e.g., 150 to 500)

# Generate mock data
data = {
    'USER_ID': [str(uuid.uuid4()) for _ in range(num_users)],
    'HEALTH_GOAL': [random.choice(health_goals) for _ in range(num_users)],
    'WEEKLY_BUDGET': [random.uniform(min_budget, max_budget) for _ in range(num_users)]
}

df = pd.DataFrame(data)

# Round WEEKLY_BUDGET to two decimal places
df['WEEKLY_BUDGET'] = df['WEEKLY_BUDGET'].round(2)

# Preview the generated data
print(df.head())

# Save to CSV file
csv_file = 'user_train_data.csv'
df.to_csv(csv_file, index=False)
