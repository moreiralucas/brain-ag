from rest_framework.viewsets import ModelViewSet, GenericViewSet
from core.models import RuralProducer, Crops
from django.db.models import Count, Sum
from core.serializers import RuralProducerSerializer
from rest_framework import mixins, status
from rest_framework.response import Response


class RuralProducerViewset(ModelViewSet):
    queryset = RuralProducer.objects.all()
    serializer_class = RuralProducerSerializer

class DashboardViewset(GenericViewSet):

    def list(self, request, *args, **kwargs):
        total_areas = RuralProducer.objects.aggregate(
            total_agricultural_area=Sum('agricultural_area'),
            total_vegetation_area=Sum('vegetation_area')
        )

        data = {
            "total_farms_quantity": RuralProducer.objects.all().count(),
            "total_farms_hectares": sum(RuralProducer.objects.all().values_list("total_area", flat=True)),
            "per_state": RuralProducer.objects.values('state').annotate(total_farms=Count('id')).order_by('state'),
            "per_crop": Crops.objects.values("name").annotate(total_per_crop=Count("id")).order_by("name"),
            "per_land_use": total_areas,
        }

        return Response(data, status=status.HTTP_200_OK)
