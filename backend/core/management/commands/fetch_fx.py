import datetime as dt
import requests

from django.core.management.base import BaseCommand
from core.models import FXRate

# Free daily reference rates (ECB-based) via Frankfurter
BASE_URL = "https://api.frankfurter.app"


class Command(BaseCommand):
    help = "Fetch daily FX rates and store them in the database (reference rates)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--pairs",
            nargs="+",
            default=["EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD", "AUDUSD"],
            help="Currency pairs like EURUSD GBPUSD USDJPY",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="How many past days to fetch (approx).",
        )

    def handle(self, *args, **opts):
        pairs = [p.upper().strip() for p in opts["pairs"]]
        days = int(opts["days"])

        end = dt.date.today()
        start = end - dt.timedelta(days=days)

        self.stdout.write(f"Fetching daily FX for {pairs} from {start} to {end} ...")

        created_total = 0
        updated_total = 0

        for pair in pairs:
            base = pair[:3]
            quote = pair[3:]

            # Frankfurter uses base + symbols
            url = f"{BASE_URL}/{start}..{end}"
            params = {"from": base, "to": quote}

            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()

            rates = data.get("rates", {})
            for date_str, d in rates.items():
                rate = d.get(quote)
                if rate is None:
                    continue

                date_obj = dt.date.fromisoformat(date_str)
                obj, created = FXRate.objects.update_or_create(
                    pair=pair,
                    date=date_obj,
                    defaults={"rate": float(rate)},
                )
                if created:
                    created_total += 1
                else:
                    updated_total += 1

            self.stdout.write(f"  {pair}: {len(rates)} rows")

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created={created_total}, Updated={updated_total}"
        ))
