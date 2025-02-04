from rest_framework import serializers
from .models import Job, MarkingJob, Performance, Employee, Client, Hall

"""
Serializers in Django REST Framework (DRF):

Serializers in DRF allow complex data types, such as Django model instances or querysets, 
to be converted to easily renderable formats, typically JSON, and vice versa. They provide 
a mechanism to validate the converted data against a set of rules to ensure data integrity.

Here's a breakdown of the serializers we're using:

1. `ModelSerializer`: A type of serializer that automatically handles the creation of 
   serializers for a given model. It provides default implementations for the create() and 
   update() methods.

   For instance:
   - `JobSerializer`: Serializes the Job model. The `j_performance` field is marked as read-only.
   - `MarkingJobSerializer`: Serializes the MarkingJob model.
   - `PerformanceSerializer`: Serializes the Performance model.
   - `ClientSerializer`: Serializes the Client model.
   - `HallSerializer`: Serializes the Hall model.
   - `EmployeeSerializer`: Serializes the Employee model.

Attributes:
- `model`: Defines the model class that the serializer will operate on.
- `fields`: Specifies which fields from the model should be included in the serialized output.
  - `'__all__'` means all fields of the model will be included.
- `read_only_fields`: Lists the fields that should be treated as read-only and cannot be modified.

Usage:
To serialize a model instance or queryset, simply pass it to the serializer and then access the `data` attribute.
To deserialize data, you'd pass the data to the serializer and then call the `is_valid()` method followed by the `save()` method.

Overall, serializers make it easier to work with HTTP methods (GET, POST, PUT, DELETE), 
by converting complex data into a format that can be easily rendered into a content type 
that clients can work with (like JSON), and for validating incoming data before saving it 
to the database.
"""

class JobSerializer(serializers.ModelSerializer):
    venue_name = serializers.CharField(source='j_client.venue_name', read_only=True)
    region = serializers.CharField(source='j_client.region', read_only=True)
    j_client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all(), write_only=True)

    class Meta:
        model = Job
        fields = ['id', 'j_client', 'venue_name', 'show', 'marking_days', 'region', 'start_date', 'end_date', 'status']



class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class MarkingJobSerializer(serializers.ModelSerializer):
    mj_hall = serializers.PrimaryKeyRelatedField(queryset=Hall.objects.all())
    mj_job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), write_only=True)
    show = serializers.CharField(source='mj_job.show', read_only=True)
    class Meta:
        model = MarkingJob
        fields = [
            'id', 'mj_hall','mj_job', 'colour', 'show',
            'pre_corners', 'pre_numbers', 'pre_others', 'pre_area', 
            'fin_corners', 'fin_numbers', 'fin_others', 'fin_area'
        ]

    def to_representation(self, instance):
        # First get the original representation
        ret = super().to_representation(instance)

        # Then change the mj_hall field from ID to the full object
        ret['mj_hall'] = HallSerializer(instance.mj_hall).data
        return ret



class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
    
class EmployeeSerializer(serializers.ModelSerializer):

    def validate_type(self, value):
        allowed_types = [choice[0] for choice in Employee.TYPE_CHOICES]
        if value not in allowed_types:
            raise serializers.ValidationError(f"Invalid type '{value}'. Allowed types are: {', '.join(allowed_types)}.")
        return value

    class Meta:
        model = Employee
        fields = '__all__'

