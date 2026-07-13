from django.shortcuts import get_object_or_404, redirect, render
from .models import Havaalanlari, Ucuslar, Yolcular, YolcuUcuslari


def anasayfa(request):
    ucuslar = Ucuslar.objects.select_related('kalkis_havaalani_id', 'varis_havaalani_id').all()
    return render(request, 'havayolları/index.html', {
        'ucuslar': ucuslar,
        'kalkis_havaalanlari': Havaalanlari.objects.all().order_by('sehir'),
        'varis_havaalanlari': Havaalanlari.objects.all().order_by('sehir'),
    })


def flight_search(request):
    flights = Ucuslar.objects.select_related('kalkis_havaalani_id', 'varis_havaalani_id')

    from_airport_id = request.GET.get('from_airport')
    to_airport_id = request.GET.get('to_airport')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if from_airport_id:
        flights = flights.filter(kalkis_havaalani_id_id=from_airport_id)
    if to_airport_id:
        flights = flights.filter(varis_havaalani_id_id=to_airport_id)
    if start_date:
        flights = flights.filter(kalkis_tarihi=start_date)
    if end_date:
        flights = flights.filter(varis_tarihi=end_date)

    return render(request, 'havayolları/flight_search.html', {'flights': flights})


def bilet_kaydet(request):
    selected_flight = None
    flight_id = request.POST.get('flight_id') or request.GET.get('flight_id')
    if flight_id:
        selected_flight = get_object_or_404(Ucuslar, pk=flight_id)

    if request.method == 'POST':
        isim = request.POST.get('isim')
        soyisim = request.POST.get('soyisim')
        dogum_tarihi = request.POST.get('dogum_tarihi')
        pasaport_no = request.POST.get('pasaport_no')

        if isim and soyisim and dogum_tarihi and pasaport_no:
            yolcu = Yolcular.objects.create(
                isim=isim,
                soyisim=soyisim,
                dogum_tarihi=dogum_tarihi,
                pasaport_no=pasaport_no,
            )
            ucus = selected_flight or Ucuslar.objects.first()
            if ucus:
                YolcuUcuslari.objects.create(yolcu=yolcu, ucus=ucus)
            return redirect('/')

    return render(request, 'havayolları/bilet_al.html', {'selected_flight': selected_flight})
