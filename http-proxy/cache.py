import time
import sys
from operator import itemgetter


class Cache:
    def __init__(self, expire, max_size):
        self.__cache = {}
        self.__expire = expire
        self.__max_size = max_size

    def get(self, request):
        if request.can_cache() and not self.__check_expire(request):
            return self.__cache.get(request)
        else:
            return None

    def put(self, request, response):
        if request.can_cache() and response.can_cache():
            self.__cache[request] = (time.time(), response)

    def __check_expire(self, request):
        set_time, value = self.__cache.get(request)
        if set_time is not None:
            if set_time + self.__expire > time.time():
                self.__cache.pop(request)
                return True
            else:
                return False
        else:
            return True

    def __check_cache_size(self):
        return sys.getsizeof(self.__cache) < self.__max_size

    def __clear_old_cache(self):
        if not self.__check_cache_size():
            for key, set_time, value in self.__cache.items():
                if set_time + self.__expire > time.time():
                    self.__cache.pop(key)
        if not self.__check_cache_size():
            sorted_by_time_cache = sorted(self.__cache.items(), key=itemgetter(1))
            for key, value in sorted_by_time_cache:
                self.__cache.pop(key)
                if self.__check_cache_size():
                    return
