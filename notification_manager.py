class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    pass

"""

EJEMPLO DE LLAMADO A LA API DE TWILIO

curl 'https://api.twilio.com/2010-04-01/Accounts/ACc5e98f930560ce32c30a22bab371de67/Messages.json' -X POST \
--data-urlencode 'To=+5491139492506' \
--data-urlencode 'MessagingServiceSid=MG0384db0fc9d79e860ad980dfa7e2e835' \
--data-urlencode 'Body=Ahoy 👋' \
-u ACc5e98f930560ce32c30a22bab371de67:7e9ea823d21ff4e2dda8487426dbc156

"""

"""

CODIGO PARA IMPORTAR VARIABLES DEL .ENV

import os
from dotenv import load_dotenv

load_dotenv()

MY_ENV_VAR = os.getenv('MY_ENV_VAR')

"""
