from datetime import datetime
import math
from django.shortcuts import render
import json
from datetime import datetime
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from rest_framework.response import Response
from django.db.models import Q
from DataProcess.models import Client, Hall, Job, Performance
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum

def add_client(request):
    """
    This function is used to add a new client to the system.

    **Endpoint:** `/client/add`
    
    **Method:** `POST`
    
    :param request: Django HttpRequest object
    :type request: HttpRequest
    :return: JsonResponse containing client creation status and client details
    :rtype: JsonResponse

    **Example**::

        sample request:

        .. code-block:: json

            {   
                "client_name": "client1",
                "email": "client1@email.com",
                "phone": "1234567890"
            }

        if the function is successful, it will return something like this:

        .. code-block:: json

            {
                "success": "Client created successfully.",
                "client": {
                    "client_name": "client1",
                    "email": "client1@email.com",
                    "phone": "1234567890"
                }
            }
    """
    # Check if the request method is POST
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Malformed JSON'}, status=400)
        # Get the client details from the request
        venue_name = data.get('venue_name')
        email = data.get('email')
        phone = data.get('phone')
        region = data.get('region')
        halls = data.get('halls')
        # Create a new client
        try:
            client = Client(venue_name=venue_name, email=email, phone=phone, region=region)
            client.save()
            if halls:
                halls_insert = list()
                for each_hall in halls:
                    halls_insert.append(Hall(hall=each_hall['hall'], area=each_hall['area'], h_client=client))
                Hall.objects.bulk_create(halls_insert)
            client.save()

        except Exception as e:
            return JsonResponse({'error': f'Failed to create client. {e}'}, status=400)

        # Return a success response
        return JsonResponse({'success': f'Client created successfully.', 'client': client.to_dict()}, status=201)

    # Return an error response if the request method is not POST
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def update_client(request):
    """
    This function is used to update an existing client in the system.

    **Endpoint:** `/client/update/<int:pk>`
    
    **Method:** `POST`
    
    :param request: Django HttpRequest object
    :param pk: primary key of the client to be updated
    :type request: HttpRequest
    :type pk: int
    :return: JsonResponse containing client update status and client details
    :rtype: JsonResponse

    **Example**::

        sample request:

        .. code-block:: json

            {   
                "client_name": "client2",
                "email": "client2@email.com",
                "phone": "0987654321"
            }

        if the function is successful, it will return something like this:

        .. code-block:: json

            {
                "success": "Client updated successfully.",
                "client": {
                    "client_name": "client2",
                    "email": "client2@email.com",
                    "phone": "0987654321"
                }
            }
    """
    # ... existing code ...

    if request.method == "PATCH":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Malformed JSON'}, status=400)

        id = data.get('id')
        venue_name = data.get('venue_name')
        email = data.get('email')
        phone = data.get('phone')
        region = data.get('region')
        updated_halls = data.get('halls')

        try:
            client = Client.objects.get(id=int(id))
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'Client with ID {id} does not exist.'}, status=404)

        client.venue_name = venue_name
        client.email = email
        client.phone = phone
        client.region = region

        # Process each hall in the update request
        new_halls = []
        for each_hall in updated_halls:
            try:
                # Check if the hall already exists
                existing_hall = Hall.objects.get(h_client=client, hall=each_hall['hall'])
                existing_hall.area = each_hall['area']
                existing_hall.save()
            except Hall.DoesNotExist:
                # If hall does not exist, prepare it for bulk creation
                new_halls.append(Hall(hall=each_hall['hall'], area=each_hall['area'], h_client=client))

        # Bulk create new halls
        if new_halls:
            Hall.objects.bulk_create(new_halls)

        client.save()

        return JsonResponse({'success': 'Client updated successfully.', 'client': client.to_dict()}, status=201)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def get_client(request, client_id):
    if request.method == 'GET':
        if client_id is None:
            return JsonResponse({'error': 'Malformed JSON'}, status=400)
        try:
            client = Client.objects.get(id=int(client_id))
            halls = Hall.objects.filter(h_client=client)
            halls_list = [hall.to_dict() for hall in halls]
            client = client.to_dict()
            client['halls'] = halls_list
            return JsonResponse({'client': client}, status=200)
        except Exception as e:
            return JsonResponse({'error': f'client.{e} does not exist'}, status=404)


def delete_client(request, client_id):
    if request.method == 'DELETE':
        if client_id is None:
            return JsonResponse({'error': 'Malformed JSON'}, status=400)
        try:
            Client.objects.get(id=int(client_id)).delete()
            return JsonResponse({'success': 'The client has been deleted'}, status=202)
        except Exception as e:
            return JsonResponse({'error': f'client.{e} failed to be deleted'}, status=404)

def client_list(request, items_per_page=10, page=1):
    """
    This function is used to retrieve all clients from the system.

    **Endpoint:** `/clients/`
    
    **Method:** `GET`
    
    :param request: Django HttpRequest object
    :type request: HttpRequest
    :return: JsonResponse containing client retrieval status and list of all clients
    :rtype: JsonResponse

    **Example**::

        sample request:

        .. code-block:: json

            {}

        if the function is successful, it will return something like this:

        .. code-block:: json

            {
                "success": "Clients retrieved successfully.",
                "clients": [
                    {
                        "client_name": "client1",
                        "email": "client1@email.com",
                        "phone": "1234567890"
                    },
                    {
                        "client_name": "client2",
                        "email": "client2@email.com",
                        "phone": "0987654321"
                    }
                    # Additional client objects...
                ]
            }
    """
    if request.method == "GET":
        try:
            end_index = page * items_per_page
            start_index = end_index - items_per_page

            clientsGet = Client.objects.all()[start_index:end_index]
            clientsSend = list()
            num_result = Client.objects.all().count()

            for client in clientsGet:
                clientsSend.append(client.to_dict())
            # Return clients.
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to retrieve clients. {e}'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


def get_client_name_list(request):
    
    if request.method == "GET":
        try:
            # Get all the clients.
            clientsGet = Client.objects.all()
            clientsSend = list()
            for client in clientsGet:
                clientsSend.append({"id" : client.id, "venue_name" : client.venue_name})
            # Return clients.
            return JsonResponse({'clients': clientsSend}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to retrieve clients. {e}'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def client_list_search(request, items_per_page, page, search):

    if request.method == 'GET':
        end_index = page * items_per_page
        start_index = end_index - items_per_page
        try:
            clientsGet = Client.objects.filter(
                Q(region__icontains=search) | Q(venue_name__icontains=search))[start_index:end_index]
            num_result = clientsGet.count()
            clientsSend = list()
            for client in clientsGet:
                clientsSend.append(client.to_dict())
            # Return clients.
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend}, status=200)

        except Exception as e:
            return JsonResponse({'error': f'Failed to retrieve clients. {e}'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def client_list_sort(request, items_per_page, page, attribute, order):
        
    if request.method == 'GET':
        end_index = page * items_per_page
        start_index = end_index - items_per_page
        num_result = Client.objects.all().count()

        if order == "ASC":
            desc = ""
        elif order == "DSC":
            desc = "-"

        if attribute == 'region':
            clients = Client.objects.order_by(desc + "region")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'venue_name':
            clients = Client.objects.order_by(desc + "venue_name")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'email':
            clients = Client.objects.order_by(desc + "email")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'phone':
            clients = Client.objects.order_by(desc + "phone")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'id':
            clients = Client.objects.order_by(desc + "id")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        else:
            return JsonResponse({'error': 'Invalid sort term.'}, status=400)
        
def client_list_sort_search(request, items_per_page, page, search, attribute, order):
        
    if request.method == 'GET':
        end_index = page * items_per_page
        start_index = end_index - items_per_page
        num_result = Client.objects.all().count()

        if order == "ASC":
            desc = ""
        elif order == "DSC":
            desc = "-"

        if attribute == 'region':
            clients = Client.objects.filter(
                Q(region__icontains=search) | Q(venue_name__icontains=search)).order_by(desc + "region")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'venue_name':
            clients = Client.objects.filter(
                Q(region__icontains=search) | Q(venue_name__icontains=search)).order_by(desc + "venue_name")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'email':
            clients = Client.objects.filter(
                Q(region__icontains=search) | Q(venue_name__icontains=search)).order_by(desc + "email")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        elif attribute == 'phone':
            clients = Client.objects.filter(
                Q(region__icontains=search) | Q(venue_name__icontains=search)).order_by(desc + "phone")[start_index:end_index]
            clientsSend = list()
            for client in clients:
                clientsSend.append(client.to_dict())
            return JsonResponse({'total_num_pages': math.ceil(num_result / items_per_page), 'clients': clientsSend})
        else:
            return JsonResponse({'error': 'Invalid sort term.'}, status=400)
        

def client_data(request):
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            venue_names = body_data.get('venue_names', [])
            post_pandemic = body_data.get('postPandemic', None)
            year = body_data.get('year', None)
            
            if not venue_names:
                return JsonResponse({'error': 'At least one venue name is required'}, status=400)
            
            clients_data = []

            post_pandemic_start_date = datetime(2020, 7, 1)  # Adjust this as per the actual start date of the pandemic
            
            for venue_name in venue_names:
                try:
                    client = Client.objects.get(venue_name=venue_name)
                    
                    jobs = Job.objects.filter(j_client=client)

                    if year:
                        start_date = datetime(year, 1, 1)
                        end_date = datetime(year, 12, 31)

                        # Check for the post-pandemic and specific year condition
                        if post_pandemic is False and start_date >= post_pandemic_start_date:
                            return JsonResponse({'message': 'No data available for pre-pandemic in the selected year'}, status=200)
                        if post_pandemic and start_date < post_pandemic_start_date:
                            return JsonResponse({'message': 'No data available for post-pandemic in the selected year'}, status=200)
                        jobs = jobs.filter(start_date__gte=start_date, start_date__lte=end_date)

                    if post_pandemic is not None:
                        if post_pandemic:
                            jobs = jobs.filter(start_date__gte=post_pandemic_start_date)
                        else:
                            jobs = jobs.filter(start_date__lt=post_pandemic_start_date)


                    performance_data = {
                        'total_fte_days': 0,
                        'total_intern_days': 0,
                        'total_marks': 0,
                        'total_days': 0
                    }

                    for job in jobs:
                        if hasattr(job, 'performance'):
                            performance = job.performance
                            performance_data['total_marks'] += performance.total_marks
                            performance_data['total_days'] += performance.marks_window
                            performance_data['total_fte_days'] += performance.fte_engineer_days
                            performance_data['total_intern_days'] += performance.intern_helper_days

                    average_marks_per_day = performance.marks_day / performance_data['total_days'] if performance_data['total_days'] > 0 else 0

                  
                    monthly_jobs = jobs.annotate(month=TruncMonth('start_date')).values('month').annotate(
                        total_fte_days=Sum('performance__fte_engineer_days'),
                        total_intern_days=Sum('performance__intern_helper_days')
                    )

                    monthly_working_days = [
                        {
                            "month": job['month'].strftime("%B"),
                            "year": job['month'].year,
                            "total_fte_days": job['total_fte_days'],
                            "total_intern_days": job['total_intern_days']
                        }
                        for job in monthly_jobs
                    ]

                    client_data = {
                        'venue_name': venue_name,
                        'average_marks_per_day': average_marks_per_day,
                        'total_fte_days': performance_data['total_fte_days'],
                        'total_intern_days': performance_data['total_intern_days'],
                        'monthly_working_days': monthly_working_days
                    }

                    clients_data.append(client_data)

                except Client.DoesNotExist:
                    clients_data.append({'venue_name': venue_name, 'error': 'Client does not exist'})
            
            return JsonResponse({'clients': clients_data}, status=200)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


