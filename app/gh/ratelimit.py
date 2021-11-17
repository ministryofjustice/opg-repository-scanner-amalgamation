from pprint import pp
import time
from datetime import datetime, timedelta
from github import Github
from github import RateLimitExceededException
from github.Rate import Rate
from github.RateLimit import RateLimit
from out import out

class limiter:
    # create an Rate class as we'll use this struct
    LIMITER = Rate(None, {}, {'limit':5000, 'remaining':5000}, True)

    @staticmethod
    def update(connection:Github) -> RateLimit:
        """
        """
        ratelimit = connection.get_rate_limit()
        out.debug(f"Rate limit data: [{ratelimit.core.remaining}/{ratelimit.core.limit}] reset: [{ratelimit.core.reset}]")
        limiter.LIMITER = ratelimit.core
        return limiter.LIMITER

    @staticmethod
    def pause(connection:Github, extend:int = 5) -> datetime:
        """
        """
        date = limiter.LIMITER.reset + timedelta(seconds=extend)
        now = datetime.utcnow()
        pause_for = (date - now).total_seconds()
        out.debug(f"Pausing execution for [{pause_for}] seconds until [{date}]")
        time.sleep(pause_for)
        return date

    @staticmethod
    def check(connection:Github, refresh:bool = True):
        """
        """
        try:
            if refresh:
                limiter.update(connection)

            if limiter.LIMITER.remaining <= 1:
                limiter.pause(connection, 5)

        except RateLimitExceededException:
            limiter.pause()

        return
