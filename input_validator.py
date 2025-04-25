import json
import re
import logging

# Setup basic logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Define suspicious patterns for simple prompt injection detection
SUSPICIOUS_PATTERNS = [
    r"ignore.*previous", 
    r"disregard.*above",
    r"forget.*instructions",
    r"repeat after me",
    r"override.*rules",
    r"bypass.*content",
    r"you are not an AI",
    r"simulate a scenario",
    r"pretend.*system",
    r"confess you are",
    r"act as a human",
    r"jailbreak"
]

def detect_prompt_injection(prompt: str) -> bool:
    """
    Check if the prompt matches known suspicious injection patterns.
    """
    prompt = prompt.lower()
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, prompt):
            logger.warning(f"Potential injection detected: pattern='{pattern}' prompt='{prompt}'")
            return True
    return False

def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        if event.get("body"):
            body = json.loads(event["body"])
            prompt = body.get("prompt", "")
        else:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing body or prompt in request."})
            }
        
        if not prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Prompt is empty or missing."})
            }

        # Perform prompt injection detection
        if detect_prompt_injection(prompt):
            return {
                "statusCode": 403,
                "body": json.dumps({"error": "Potential prompt injection detected. Request blocked."})
            }

        # If safe, return the validated prompt
        return {
            "statusCode": 200,
            "body": json.dumps({"validated_prompt": prompt})
        }

    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}", exc_info=True)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error."})
        }
