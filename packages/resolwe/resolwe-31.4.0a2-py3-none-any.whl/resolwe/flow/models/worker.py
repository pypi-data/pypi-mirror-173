"""Worker data model representing the state of the executor."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.db import models


class Worker(models.Model):
    """Stores information about worker."""

    STATUS_PREPARING = "PP"
    STATUS_FINISHED_PREPARING = "FP"
    STATUS_PROCESSING = "PR"
    STATUS_NONRESPONDING = "NR"
    STATUS_COMPLETED = "CM"
    STATUS_ERROR_PREPARING = "EP"

    FINAL_STATUSES = (
        STATUS_COMPLETED,
        STATUS_ERROR_PREPARING,
        STATUS_NONRESPONDING,
    )

    STATUS_CHOICES = (
        (STATUS_PROCESSING, "Processing data"),
        (STATUS_NONRESPONDING, "Unresponsive"),
        (STATUS_PREPARING, "Preparing data"),
        (STATUS_COMPLETED, "Finished"),
    )

    started = models.DateTimeField(auto_now=True)
    finished = models.DateTimeField(null=True)
    data = models.OneToOneField(
        "flow.Data", on_delete=models.CASCADE, related_name="worker"
    )
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)

    def terminate(self):
        """Terminate the running worker."""

        # Can only terminate running processes.
        if self.status != self.STATUS_PROCESSING:
            print("Wrong status, no go")
            print(self.status)
            return

        packet = {"type": "terminate", "identity": str(self.data.id).encode()}
        from resolwe.flow.managers.state import LISTENER_CONTROL_CHANNEL

        print("Sending terminate signal")
        print("On ", LISTENER_CONTROL_CHANNEL)
        async_to_sync(get_channel_layer().send)(LISTENER_CONTROL_CHANNEL, packet)
        print("Sent terminate signal")

    def __str__(self):
        """Return the string representation."""
        return f"Worker(status={self.status}, data={self.data}, status={self.status})"
