import json
import queue

announcers = {}


class MessageAnnouncer:
    def __init__(self):
        self.listeners = []

    def listen(self):
        print("Adding listener")
        q = queue.Queue(maxsize=5)
        self.listeners.append(q)
        q.put_nowait(
            format_sse(data=json.dumps({"message": "You have successfully connected"}))
        )
        return q

    def announce(self, msg):
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]


def format_sse(data: str, event=None) -> str:
    msg = f"data: {data}\n\n"
    if event is not None:
        msg = f"event: {event}\n{msg}"
    return msg
