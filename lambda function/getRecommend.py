import boto3
import json

def lambda_handler(event, context):
    personalize_runtime = boto3.client('personalize-runtime')
    campaign_arn = 'arn:aws:personalize:us-east-1:xxxxxx:campaign/campaign-latest'
    user_id = '690d042f-4605-4e48-a7b4-8b452dd10514'
    item_id = 'h9nuvIu8TyrQcYy8J1AOxg'

    response = personalize_runtime.get_personalized_ranking(
        campaignArn=campaign_arn,
        userId=user_id,
        inputList=[item_id]
    )
    predicted_score = response['personalizedRanking'][0]['score']
    print(f"Predicted score for item {item_id} and user {user_id} is: {predicted_score}")

    return {
        'statusCode': 200,
        'body': json.dumps('Recommendations retrieved successfully!')
    }
