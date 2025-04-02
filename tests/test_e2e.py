import pytest
import logging
from common.api_call import api_call


# ----------------------------------------------------------------------------------------------------------------------
# E2E SUITE
# To perform E2E validation when doing integration testing.
# Verify data integrity after POSR or PUT operations. Make sure data is showing the expected information in the other
# system.
# Do CRUD end to end: POST -> GET -> PUT -> GET -> DELETE -> GET
# Do not forget that there might be cache problems, per example, if cache is invalidated after a data change. Sometimes
# TEST environment do not have cache configured but PROD does.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
