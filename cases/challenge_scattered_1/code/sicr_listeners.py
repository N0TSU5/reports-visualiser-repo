
class EventDispatcher:
    @staticmethod
    def emit(event_name, context):
        if event_name == 'evaluate_sicr':
            return context['dpd'] >= context['backstop']
