from datetime import datetime
from stash import Stash


def log_motion_event():
    motion_events = Stash('motion_events')
    motion_events.add({'date': datetime.utcnow().isoformat()})
