import datetime
import json

import requests
from django.conf import settings
from django.views.generic import TemplateView


class NasaView(TemplateView):
    template_name = "nasa.html"

    MAX_RANGE_DAYS = 7

    CACHE_EXPIRY = 60 * 60

    def dispatch(self, request, *args, **kwargs):
        self.context = {"data": None, "error": None}
        api_key = getattr(settings, "NASA_API_KEY", None)
        if not api_key:
            self.context["error"] = "Missing NASA_API_KEY in settings."
            return super().dispatch(request, *args, **kwargs)

        if request.method == "GET":
            start_date_str = request.GET.get("start_date")
            end_date_str = request.GET.get("end_date")
            asteroid_id = request.GET.get("asteroid_id")

            if asteroid_id:
                self.context["data"] = self.fetch_asteroid_data(asteroid_id, api_key)
            else:
                if start_date_str:
                    start_date = datetime.datetime.fromisoformat(start_date_str)
                    if end_date_str:
                        end_date = datetime.datetime.fromisoformat(end_date_str)

                        delta = (end_date - start_date).days
                        if delta < 0:
                            self.context["error"] = (
                                "end_date cannot be before start_date."
                            )
                            return super().dispatch(request, *args, **kwargs)
                        if delta > self.MAX_RANGE_DAYS:
                            self.context["error"] = (
                                f"Date range cannot exceed {self.MAX_RANGE_DAYS} days."
                            )
                            return super().dispatch(request, *args, **kwargs)

                        if self.request.GET.get("CLEAN") == 9:
                            combined_data = {}
                            current_day = start_date
                            while current_day <= end_date:
                                day_str = current_day.strftime("%Y-%m-%d")
                                feed_data = self.fetch_nasa_feed(day_str, api_key)
                                if "near_earth_objects" in feed_data:
                                    for day_key, objs in feed_data[
                                        "near_earth_objects"
                                    ].items():
                                        if day_key not in combined_data:
                                            combined_data[day_key] = []
                                        combined_data[day_key].extend(objs)

                                current_day += datetime.timedelta(days=1)
                        else:
                            data = self.fetch_nasa_feed_between(
                                start_date_str, end_date_str, api_key
                            )
                            if "near_earth_objects" in data:
                                combined_data = {
                                    f"{start_date_str} - {end_date_str}": []
                                }
                                for day_key, objs in data["near_earth_objects"].items():
                                    combined_data[
                                        f"{start_date_str} - {end_date_str}"
                                    ].extend(objs)
                            else:
                                combined_data = data
                        self.context["data"] = {
                            "near_earth_objects": combined_data,
                            "flare": requests.get(
                                f"https://api.nasa.gov/DONKI/FLR?startDate={start_date_str}&endDate={end_date_str}&api_key={api_key}"
                            ).json(),
                        }
                    else:
                        day_str = start_date.strftime("%Y-%m-%d")
                        self.context["data"] = self.fetch_nasa_feed(day_str, api_key)
                else:
                    self.context["error"] = (
                        "Please provide at least an asteroid_id OR a start_date."
                    )
        else:
            self.context["error"] = "Method not allowed. Only GET is supported."

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.context)
        return context

    def fetch_asteroid_data(self, asteroid_id, api_key):
        url = f"https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}?api_key={api_key}"
        data = self.get_data(url)
        return data

    def fetch_nasa_feed(self, date_str, api_key):
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={date_str}&end_date={date_str}&api_key={api_key}"
        data = self.get_data(url)
        return data

    def fetch_nasa_feed_between(self, start_date_str, end_date_str, api_key):
        url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date_str}&end_date={end_date_str}&api_key={api_key}"
        data = self.get_data(url)
        return data

    def get_data(self, url):
        print(f"Fetching from NASA: {url}")
        try:
            response = requests.get(url, timeout=5)
        except requests.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}

        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"error": "Invalid JSON in NASA response"}

        return data
