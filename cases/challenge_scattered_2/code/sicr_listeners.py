import sicr_listeners_hop1
class EventDispatcher:
    @staticmethod
    def emit(event_name, context):
        if event_name == 'evaluate_sicr':
            return sicr_listeners_hop1.execute(context)
