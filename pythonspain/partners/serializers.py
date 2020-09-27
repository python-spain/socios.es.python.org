from rest_framework import serializers

from .models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = "__all__"
        read_only_fields = [
            "number",
            "request_date",
            "approval_date",
            "has_board_directors_charge",
            "charge",
            "is_founder",
            "is_active",
        ]
