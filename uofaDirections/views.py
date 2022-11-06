from django.http import HttpResponse
from django.shortcuts import render, redirect
from .edgeCalculator import *
from django.templatetags.static import static

def home(request):
    return render(request, 'index.html')
def routeResponse(request):
    response_data = {}
    start = request.GET.get('start')
    end = request.GET.get("end")
    doors, N = generateJson("static/MapData-Buildings.csv")
    peds = getPedways("static/MapData-Pedways.csv")
    ped_edges = addPeds(peds,doors,N)

    name_to_door = { d["name"]:d["id"] for reg in doors for d in doors[reg]}
    N = len(name_to_door)

    int_edges = interalDist(doors)
    ext_edges = externalDist(doors)

    all_edges = reid_edges(int_edges,name_to_door) + ext_edges + ped_edges


    route = search(all_edges, doors[start][0]["id"], doors[end][0]["id"], N)
    return HttpResponse(json.dumps(route))