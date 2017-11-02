import os

import vcr

# use environment variable to enable network tests
LIMBO_NETWORK_TESTS = os.environ.get('LIMBO_NETWORK_TESTS', False)


def before_record_callback(request):
    """
    Run tests using network API calls if LIMBO_NETWORK_TESTS; otherwise use vcr fixtures
    """
    if LIMBO_NETWORK_TESTS:
        return None
    else:
        return request


VCR = vcr.VCR(
    before_record=before_record_callback
)
