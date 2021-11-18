import pytest
import github
import math
from datetime import timedelta, datetime
from pprint import pp
from github.Rate import Rate
from github.RateLimit import RateLimit
from github_extensions.rate_limiter import rate_limiter


def test_rate_limiter_pause():
    """
    Create mock rate limit object and use that with fake dates to test pause
    """
    before = datetime.utcnow()
    pause_for = 2
    rate = Rate(None, {}, {'limit':2, 'remaining':1, 'reset': int(before.timestamp()) }, True)

    rate_limiter.LIMITER = rate
    reset = rate_limiter.pause(pause_for)
    after = datetime.utcnow()
    # round the gap up
    gap = math.ceil( (after - before).total_seconds() )

    assert (after > before) == True
    assert (gap >= pause_for) == True
