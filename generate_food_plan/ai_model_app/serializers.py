from rest_framework import serializers

class PlanGenerationSerializer(serializers.Serializer):
    input_data = serializers.CharField()
    generated_plans = serializers.JSONField()