from collections import namedtuple

class Load: pass
class Deliver: pass
class Unload: pass
class Wait: pass

Action = namedtuple('Action', ['drone', 'type', 'item', 'dest'])
