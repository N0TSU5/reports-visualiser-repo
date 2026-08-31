def execute(ctx):
    return ctx['flag'] or ctx['dpd'] >= ctx['threshold']
