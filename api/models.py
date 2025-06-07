from django.db import models

class Robot(models.Model):
    uuid = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or self.uuid


class Sensor(models.Model):
    SENSOR_TYPES = [
        ("camera", "Camera"),
        ("lidar", "LiDAR"),
        ("gps", "GPS"),
        ("imu", "IMU"),
        ("ultrasonic", "Ultrasonic"),
    ]

    robot = models.ForeignKey(Robot, related_name="sensors", on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict)  # e.g., {"fov": 90, "hz": 30}
    last_heartbeat = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.robot.uuid} - {self.sensor_type}"


class SensorData(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()  # or a file/image path, depending on sensor

    class Meta:
        indexes = [
            models.Index(fields=["sensor", "timestamp"]),
        ]
