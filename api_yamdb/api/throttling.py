from rest_framework.throttling import UserRateThrottle


class TwoRequestsPerUserThrottle(UserRateThrottle):
    rate = '2/day'
