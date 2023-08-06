import os
import requests

from cc_py_commons.config.env import app_config
from cc_py_commons.utils.logger import logger

MERCURY_URL = os.environ.get("MERCURY_URL")
MERCURY_TOKEN = os.environ.get("MERCURY_TOKEN")


def execute(params):
	url = f"{app_config.MERCURY_URL}/lanePricing"
	token = f"Bearer {app_config.MERCURY_TOKEN}"
	headers = {
		"Authorization": token
	}
	response = requests.get(url, params=params, headers=headers)

	if response.status_code != 200:
		logger.warning(
			f"Lane Pricing lookup failed for params: {params} - {response.status_code}:{response.text}")
		return None

	return response.json()
