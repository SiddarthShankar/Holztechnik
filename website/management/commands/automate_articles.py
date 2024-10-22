from django.core.management.base import BaseCommand
from django.db.models import Q
from website.models import OrderSpecs, Picking 

class Command(BaseCommand):
    help = 'Check if article string matches any of the specified strings, and create Picking entries with specific items and quantities'

    def handle(self, *args, **kwargs):
        search_strings = ['Drawer', 'Cupboard', 'Locker']

        query = Q()
        for string in search_strings:
            query |= Q(article__icontains=string)
            
        matched_order_specs = OrderSpecs.objects.filter(query)

        if matched_order_specs.exists():
            self.stdout.write(self.style.SUCCESS(f"Articles matching '{', '.join(search_strings)}' found. Creating Picking entries."))
            for order_spec in matched_order_specs:
                self.create_picking_entries(order_spec)
            self.stdout.write(self.style.SUCCESS(f"Successfully created Picking entries with specific items and quantities."))
        else:
            self.stdout.write(self.style.WARNING(f"No articles matching any of '{', '.join(search_strings)}' found"))

    def create_picking_entries(self, order_spec):
        article_lower = order_spec.article.strip().lower() 

        def update_or_create_picking(item_to_pick, quantity):
            Picking.objects.update_or_create(
                order_spec=order_spec, 
                item_to_pick=item_to_pick, 
                defaults={'quantity': quantity}
            )

        if "drawer" in article_lower:
            update_or_create_picking("Sliding Rail", 2)
            update_or_create_picking("Handle", 1)

        elif "cupboard" in article_lower:
            update_or_create_picking("Hinge", 4)
            update_or_create_picking("Handle", 2)

        elif "locker" in article_lower:
            update_or_create_picking("Hinge", 2)
            update_or_create_picking("Handle", 1)
            update_or_create_picking("Locker", 1)
