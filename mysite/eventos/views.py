import json
import requests
from decouple import config
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse


# URL del API Gateway
URL_API_GATEWAY = config('API_GATEWAY_BASE');

# View menú opciones
def home(request):
    return render(request, 'eventos/home.html', {})

# View list events
def list_events(request, event_id=None):
    headers = {
        'Content-Type': 'application/json',
        'authorizationToken': 'allow'
    }
    
    if event_id:
        try:
            # Realiza una solicitud a la API para obtener los detalles del evento
            response = requests.get(f"{URL_API_GATEWAY}events?event_id={event_id}", headers=headers)
            if response.status_code == 200:
                event = response.json()  # Obtener el evento de la respuesta
                return render(request, 'eventos/edit_event.html', {'event': event})
            else:
                print(f"Error al obtener evento: {response.status_code} - {response.content.decode()}")
        except Exception as e:
            print(f"Error al conectar con la API: {str(e)}")
    
    # Si no se recibe un event_id, obtiene todos los eventos
    else:
        events = []
        try:
            response = requests.get(f"{URL_API_GATEWAY}events", headers=headers)
            if response.status_code == 200:
                events = response.json()  # Obtener la lista de eventos
            else:
                print(f"Error al obtener eventos: {response.status_code} - {response.content.decode()}")
        except Exception as e:
            print(f"Error al conectar con la API: {str(e)}")
    
        return render(request, 'eventos/list_events.html', {'events': events})
    
# crear evento
def create_event(request):
    if request.method == 'POST':
        # Datos que obtienes del formulario
        event_id = request.POST.get('event_id')
        name_event = request.POST.get('name_event')
        description = request.POST.get('description')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        max_capacity = request.POST.get('max_capacity')
        organizer = request.POST.get('organizer')
        event_status = request.POST.get('event_status')
        event_location = request.POST.get('event_location')
        
        # Datos a enviar al API Gateway
        payload = json.dumps({
            'event_id': event_id,
            'name_event': name_event,
            'description': description,
            'event_date': event_date,
            'event_time': event_time,
            'max_capacity': max_capacity,
            'organizer': organizer,
            'event_status': event_status,
            'event_location': event_location,
        })
        
        headers = {
            'Content-Type': 'application/json',
            'authorizationToken': 'allow'  # Si es necesario
        }

        # Realizar la petición al API Gateway
        response = requests.request("POST", f"{URL_API_GATEWAY}events", headers=headers, data=payload)

        if response.status_code == 201:
            messages.success(request, 'Evento creado con éxito.')
            return redirect('list_events')
        else:
            messages.error(request, 'Error al crear el evento. Inténtalo nuevamente.')

    return render(request, 'eventos/create_event.html')

# # editar evento 
def edit_event(request):
    if request.method == 'POST':    
        event_id = request.POST.get('event_id')
        name_event = request.POST.get('name_event')
        description = request.POST.get('description')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        max_capacity = request.POST.get('max_capacity')
        organizer = request.POST.get('organizer')
        event_status = request.POST.get('event_status')
        event_location = request.POST.get('event_location')
        
        payload = json.dumps({
            'event_id': event_id,
            'name_event': name_event,
            'description': description,
            'event_date': event_date,
            'event_time': event_time,
            'max_capacity': int(float(max_capacity)),
            'organizer': organizer,
            'event_status': event_status,
            'event_location': event_location,
        })
                
        headers = {
            'Content-Type': 'application/json',
            'authorizationToken': 'allow'
        }
        
        response = requests.put(f"{URL_API_GATEWAY}events", headers=headers, data=payload)        
       
        if response.status_code == 200:
            messages.success(request, 'Evento editado con éxito.')
            return redirect('list_events')
        else:
            messages.error(request, 'Error al crear el evento. Inténtalo nuevamente.')
            return redirect('list_events')
    return render(request, 'eventos/list_events.html')

# eliminar evento
def delete_event(request, event_id):
    try:
        # Realizar la solicitud DELETE a la API Gateway
        payload = json.dumps({
            "event_id": event_id
        })
        
        headers = {
            'Content-Type': 'application/json',
            'authorizationToken': 'allow'
        }
        
        response = requests.request("DELETE", f"{URL_API_GATEWAY}events", headers=headers, data=payload)

        if response.status_code == 200:
            messages.success(request, 'Evento eliminado exitosamente.')
            return redirect('list_events')
        else:
            messages.error(request, 'Error al eliminar el evento.')
            return redirect('list_events')

    except Exception as e:
        print(f"Error al conectar con la API: {str(e)}")
        request.session['error_message'] = "Error al conectar con la API."
        return redirect('list_events')
    
def register_event(request):
     # Obtener los eventos activos desde la API o la base de datos
    try:
        response = requests.get('API_GATEWAY_URL')
        events = response.json()
        active_events = [event for event in events if event['status'] == 'active']
    except Exception as e:
        active_events = []
        print(f"Error al obtener eventos: {str(e)}")

    return render(request, 'eventos/register_event.html', {'active_events': active_events})
    # return render(request, 'eventos/register_event.html', {})

