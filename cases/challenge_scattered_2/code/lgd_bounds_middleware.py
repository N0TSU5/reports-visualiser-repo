import lgd_bounds_middleware_hop1
class MiddlewarePipeline:
    @staticmethod
    def process(pipeline_name, context):
        if pipeline_name == 'lgd':
            return lgd_bounds_middleware_hop1.execute(context)
