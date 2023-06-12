from rest_framework import (
    serializers
)


class GenProposalSerializer(serializers.Serializer):
    title = serializers.CharField()
    desc = serializers.CharField()
    client_n = serializers.CharField(required=False)
    type_pro = serializers.CharField(required=False)


class CheckScoreSerializer(serializers.Serializer):
    cover_desc = serializers.CharField()
    job_desc = serializers.CharField()
