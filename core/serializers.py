from decimal import Decimal
from rest_framework import serializers
from core.models import RuralProducer, Crops
from validate_docbr import CPF, CNPJ


class CropsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Crops
        fields = ("name",)
        write_only = ("producer",)


class RuralProducerSerializer(serializers.ModelSerializer):
    crops = CropsSerializer(many=True)

    class Meta:
        model = RuralProducer
        fields = ("document", "producer_name", "farm_name", "city", "state",
                "total_area", "agricultural_area", "vegetation_area", "crops")
        read_only = ("id",)

    def validate_document(self, value):
        value = value.replace(".", "").replace("-", "").replace("/", "")
        if len(value) == 11:  # CPF
            cpf = CPF()
            if not cpf.validate(value):
                raise serializers.ValidationError("Invalid CPF number.")
        elif len(value) == 14:  # CNPJ
            cnpj = CNPJ()
            if not cnpj.validate(value):
                raise serializers.ValidationError("Invalid CNPJ number.")
        else:
            raise serializers.ValidationError("Document must be either CPF (11 digits) or CNPJ (14 digits).")

        return value

    def validate(self, data):
        total_area = Decimal(data.get("total_area", 0))
        agricultural_area = Decimal(data.get("agricultural_area", 0))
        vegetation_area = Decimal(data.get("vegetation_area", 0))

        if total_area != (agricultural_area + vegetation_area):
            raise serializers.ValidationError({
                "total_area": "The total_area must be equal to the sum of agricultural_area and vegetation_area."
            })
        
        return data

    def create(self, validated_data):
        crops_data = validated_data.pop('crops')
        rural_producer = RuralProducer.objects.create(**validated_data)

        for crop_data in crops_data:
            Crops.objects.create(producer=rural_producer, **crop_data)
        return rural_producer
