from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import FXRate


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


@api_view(["GET"])
def rates(request):
    """
    Returns latest FX rates stored in DB.
    Optional query param: ?pair=EURUSD
    """
    pair = request.query_params.get("pair")
    qs = FXRate.objects.all()

    if pair:
        qs = qs.filter(pair=pair.upper())

    # return latest 50 rows (most recent dates)
    rows = qs.order_by("-date", "pair")[:50]

    out = [
        {"pair": r.pair, "date": r.date.isoformat(), "rate": r.rate}
        for r in rows
    ]
    return Response(out)

