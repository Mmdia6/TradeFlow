from collections import defaultdict
from time import monotonic
import threading, redis
from app.core.config import settings
_local=defaultdict(lambda:(0,0.0)); _lock=threading.Lock()
def allow(key:str,limit:int=10,window:int=60)->bool:
    try:
        client=redis.Redis.from_url(settings.redis_url,decode_responses=True)
        k=f"tradeflow:rate:{key}"; count=client.incr(k)
        if count==1: client.expire(k,window)
        return count<=limit
    except Exception:
        now=monotonic()
        with _lock:
            count,started=_local[key]
            if now-started>=window: _local[key]=(1,now); return True
            if count>=limit: return False
            _local[key]=(count+1,started); return True
