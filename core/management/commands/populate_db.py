from django.core.management.base import BaseCommand
from core.models import RuralProducer, Crops
from faker import Faker
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        # Define the number of records to create
        num_producers = 100
        num_crops_per_producer = 5

        for _ in range(num_producers):
            # Generate fake data
            document = fake.ssn() if random.choice([True, False]) else fake.ean13()
            producer_name = fake.name()
            farm_name = fake.company()
            city = fake.city()
            state = fake.state_abbr()
            total_area = Decimal(fake.random_number(digits=4, fix_len=True))
            agricultural_area = total_area * Decimal(random.uniform(0.1, 0.5))
            vegetation_area = total_area - agricultural_area

            # Create RuralProducer instance
            producer = RuralProducer.objects.create(
                document=document,
                producer_name=producer_name,
                farm_name=farm_name,
                city=city,
                state=state,
                total_area=total_area,
                agricultural_area=agricultural_area,
                vegetation_area=vegetation_area
            )

            # Create Crops instances
            for _ in range(num_crops_per_producer):
                Crops.objects.create(
                    name=fake.word(),
                    producer=producer
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated {num_producers} rural producers with crops'))
