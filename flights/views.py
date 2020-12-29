from django.http.response import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .models import Flight, Passenger

# Create your views here.


def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight not found.")

    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers
    })


def book(request, flight_id):
    if request.method == "POST":
        try:
            passenger_id = int(request.POST["passenger"])
            passenger = Passenger.objects.get(pk=passenger_id)
            flight = Flight.objects.get(pk=flight_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no flight chosen")
        except Flight.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: flight does not exist")
        except Passenger.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: passenger does not exist")

        passenger.flights.add(flight)

        return HttpResponseRedirect(reverse("flights:flight", args=(flight.id,)))
