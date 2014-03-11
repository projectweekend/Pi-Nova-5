from datetime import datetime
from stash import Stash


def log_motion_event():
    the_event = {
        'date': datetime.utcnow().isoformat(),
        'from': 'Nova5'
    }    
    motion_events = Stash('motion_events')
    motion_events.add(the_event)
