# charts.py

from chartjs.views.lines import BaseLineChartView
from django.utils import timezone
from .models import UserQuery
from collections import defaultdict
import datetime

class UserQueryLineChartJSONView(BaseLineChartView):

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        labels = []
        for i in range(7):
            day = timezone.now() - datetime.timedelta(days=i)
            labels.append(day.strftime('%Y-%m-%d'))
        return labels[::-1]

    def get_data(self):
        """Return 3 datasets to plot."""

        days_data = defaultdict(int)

        for i in range(7):
            day = timezone.now() - datetime.timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            days_data[day_str] = 0

        for query in UserQuery.objects.all():
            day_str = query.created_at.strftime('%Y-%m-%d')
            if day_str in days_data:
                days_data[day_str] += 1

        return [list(days_data.values())[::-1]]
