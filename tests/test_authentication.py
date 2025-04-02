import pytest
import logging
from common.api_call import api_call


# ----------------------------------------------------------------------------------------------------------------------
# AUTHENTICATION SUITE
# To validate authenticated and unauthenticated users.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
