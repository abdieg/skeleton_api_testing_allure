import pytest
import logging
from common.api_call import api_call


# ----------------------------------------------------------------------------------------------------------------------
# PERMISSION SUITE
# To validate permissions when validating entities to make sure operations work as expected.
# ----------------------------------------------------------------------------------------------------------------------


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
