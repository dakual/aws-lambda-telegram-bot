import json, logging, urllib3, os, base64

http   = urllib3.PoolManager()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def send(command, params):
    token  = os.environ.get("TELEGRAM_TOKEN")
    apiURL = f'https://api.telegram.org/bot{token}/{command}'

    try:
        message  = json.dumps(params).encode("utf-8")
        response = http.request("POST", apiURL, headers={'Content-Type': 'application/json'}, body=message)
        logger.info(response.data.decode('utf-8'))

        return response
    except Exception as e:
        return e

def lambda_handler(event, context):
    logger.info(event)

    data = event['body']
    if event["isBase64Encoded"] == True:
      data = json.dumps(event['body'])
      data = base64.b64decode(data).decode('utf-8')

    if "init" in data and data["init"] == True:
      gateway  = os.environ.get("API_GATEWAY")
      params   = {'url': gateway}
      response = send("setWebhook", params)
    else:
      data = json.loads(event['body'])
      if "message" in data:
        chat_id = data["message"]["chat"]["id"]

        if "text" in data["message"]:
          message  = data["message"]["text"]
          params   = {'chat_id': chat_id, 'text': message}
          response = send("sendMessage", params)
        else:
          message  = "Only text messages are supported!"
          params   = {'chat_id': chat_id, 'text': message}
          response = send("sendMessage", params)

    return {
        "status_code": 200,
        "response": "OK",
    }