
class MiddlewarePipeline:
    @staticmethod
    def process(pipeline_name, context):
        if pipeline_name == 'lgd':
            return min(1.0, context['unsec'] + context['addon'])
