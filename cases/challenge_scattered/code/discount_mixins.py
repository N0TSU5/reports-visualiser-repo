import discount_mixins_hop1
class DiscountingMixin:
    def _compute_discount_timing(self, months):
        return discount_mixins_hop1.execute(months)
