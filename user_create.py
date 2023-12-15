import boto3
import uuid

session = boto3.Session(
    aws_access_key_id='AKIA27C7WLPEJ4DBD4GF',
    aws_secret_access_key='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',
    region_name='us-east-1'
)

dynamodb = session.resource('dynamodb')
table_name = 'userInfo'

user_id = str(uuid.uuid4())

users = [
    {
        "user_id": user_id,
        "user_name": "John Doe",
        "Email": "johndoe@example.com",
        "WeeklyBudget": 500,
        "FavoriteRestaurants": ["yKPRuBvD3ScCc18QrZ4Y6w", "Nssb3grMQtYfJOs1HFId8A"],
        "HealthGoal": "Lose weight"
    }
]

table = dynamodb.Table(table_name)

for user in users:
    try:
        response = table.put_item(Item=user)
        print(f"User {user['user_id']} added successfully.")
    except Exception as e:
        print(f"Error adding user {user['user_id']}: {str(e)}")
