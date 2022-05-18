from unicodedata import name
from healthtogo.api.base import H2gResourceView
from flask import request
import boto3
from botocore.exceptions import ClientError
import logging

class SignUp(H2gResourceView):
    _name = 'signup'
    _uri = '/apy/signup'

    def __init__(self):
        super().__init__()
    
    def post(self):
        SENDER = "api@healthtogo.com.br"
        RECIPIENT = "atendimento@healthtogo.com.br"

        AWS_REGION = "us-east-1"
        
        SUBJECT = "(SignUp) Health To Go - User Subscription"
        BODY_TEXT = ("Name:{}\r\n"
                    "Lastname:{}\r\n"
                    "HowMetUs:{}\r\n"
                    "WorkArea:{}\r\n"
                    "Experience:{}\r\n"
                    "Email:{}\r\n"
                    "CPF:{}\r\n"
                    "CRN:{}\r\n".format()
                    )
        BODY_HTML = """<html>
        <head></head>
        <body>
        <h1>(SignUp) Health To Go - User Subscription</h1>
        <p>Name:{}</p>
        <p>Lastname:{}</p>
        <p>HowMetUs:{}</p>
        <p>WorkArea:{}</p>
        <p>Experience:{}</p>
        <p>Email:{}</p>
        <p>CPF:{}</p>
        <p>CRN:{}</p>
        </body>
        </html>
                    """.format()

        CHARSET = "UTF-8"

        client = boto3.client('ses',region_name=AWS_REGION)
        # Try to send the email.
        try:
            response = client.send_email(
                Destination={
                    'ToAddresses': [
                        RECIPIENT,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': CHARSET,
                            'Data': BODY_HTML,
                        },
                        'Text': {
                            'Charset': CHARSET,
                            'Data': BODY_TEXT,
                        },
                    },
                    'Subject': {
                        'Charset': CHARSET,
                        'Data': SUBJECT,
                    },
                },
                Source=SENDER,
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            print("Email sent! Message ID:"),
            print(response['MessageId'])
        return '', 200
