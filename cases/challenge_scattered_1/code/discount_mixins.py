
class DiscountingMixin:
    def _compute_discount_timing(self, months):
        return months // 12
