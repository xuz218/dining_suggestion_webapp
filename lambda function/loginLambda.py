import json

def lambda_handler(event, context):
    # Example credentials for demonstration purposes
    valid_username = 'cat'
    valid_password = 'cat'

    # Extract username and password from query string parameters

    username = event.get('Username')
    password = event.get('Password')
    print("The username is '", username,"'","and the password is '", password,"'")
    
    
    
    # Check if credentials are valid
    if username == valid_username and password == valid_password:
        response = {
            'statusCode': 200,
            'body': json.dumps('Valid user info.')
        }
    else:
        response = {
            'statusCode': 401,
            'body': json.dumps('Invalid user info.')
        }

    return response
