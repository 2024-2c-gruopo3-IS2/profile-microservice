import os
from datadog import initialize

# Configuración de Datadog
options = {
    'api_key': os.getenv('DATADOG_API_KEY'),
    'app_key': os.getenv('DATADOG_APP_KEY'),
    }

initialize(**options)