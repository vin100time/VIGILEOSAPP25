from rest_framework import serializers
from .models import NetworkMetric, AlertThreshold

class NetworkMetricSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    site_name = serializers.CharField(source='equipment.site.name', read_only=True)
    memory_usage_percent = serializers.ReadOnlyField()
    disk_usage_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = NetworkMetric
        fields = [
            'id', 'equipment', 'equipment_name', 'site_name', 'timestamp',
            'ping_response_time', 'packet_loss', 'bandwidth_up', 'bandwidth_down',
            'cpu_usage', 'memory_total', 'memory_used', 'memory_usage_percent',
            'disk_total', 'disk_used', 'disk_usage_percent',
            'is_online', 'connection_quality'
        ]
        read_only_fields = ['id', 'timestamp']

class NetworkMetricCreateSerializer(serializers.ModelSerializer):
    """Serializer optimisé pour la création en masse de métriques"""
    class Meta:
        model = NetworkMetric
        fields = [
            'equipment', 'ping_response_time', 'packet_loss', 
            'bandwidth_up', 'bandwidth_down', 'cpu_usage',
            'memory_total', 'memory_used', 'disk_total', 'disk_used',
            'is_online', 'connection_quality'
        ]

class AlertThresholdSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    
    class Meta:
        model = AlertThreshold
        fields = [
            'id', 'equipment', 'equipment_name',
            'ping_warning_threshold', 'ping_critical_threshold',
            'packet_loss_warning', 'packet_loss_critical',
            'cpu_warning_threshold', 'cpu_critical_threshold',
            'memory_warning_threshold', 'memory_critical_threshold',
            'disk_warning_threshold', 'disk_critical_threshold',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class MetricsSummarySerializer(serializers.Serializer):
    """Serializer pour les statistiques agrégées"""
    equipment_id = serializers.IntegerField()
    equipment_name = serializers.CharField()
    site_name = serializers.CharField()
    latest_timestamp = serializers.DateTimeField()
    avg_ping = serializers.FloatField()
    avg_cpu = serializers.FloatField()
    avg_memory_usage = serializers.FloatField()
    avg_disk_usage = serializers.FloatField()
    uptime_percentage = serializers.FloatField()
    total_measurements = serializers.IntegerField()