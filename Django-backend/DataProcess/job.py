import datetime
import math
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from django.http import JsonResponse
from django.db.models import Q
import json
from .models import Job, MarkingJob, Performance, Client, Hall, Employee

from .serializers import (
    JobSerializer,
    MarkingJobSerializer,
    PerformanceSerializer,
    HallSerializer,
    EmployeeSerializer,
    ClientSerializer,
)
from AccountManagement.permissions import RoleBasedPermission
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([RoleBasedPermission])
def job_list(request, items_per_page=10, page=1):
    """
    Handle listing all jobs or adding a new job.

    - GET: Return a list of all jobs.
    - POST: Add a new job to the system.
    """

    if request.method == "GET":
        end_index = page * items_per_page
        start_index = end_index - items_per_page

        num_result = Job.objects.all().count()
        jobs = Job.objects.all()[start_index:end_index]
        serializer = JobSerializer(jobs, many=True)
        return JsonResponse(
            {
                "total_num_pages": math.ceil(num_result / items_per_page),
                "jobs": serializer.data,
            }
        )

    elif request.method == "POST":
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def job_list_sort(request, items_per_page, page, attribute, order):
    """
    Handle listing all jobs order by a particular attribute

    - GET: Return a list of all jobs with matching search term
    """

    if request.method == "GET":
        end_index = page * items_per_page
        start_index = end_index - items_per_page
        num_result = Job.objects.all().count()

        if order == "ASC":
            desc = ""
        elif order == "DSC":
            desc = "-"

        if attribute == "region":
            jobs = Job.objects.order_by(desc + "j_client__region")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "venue_name":
            jobs = Job.objects.order_by(desc + "j_client__venue_name")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "start_date":
            jobs = Job.objects.order_by(desc + "start_date")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "end_date":
            jobs = Job.objects.order_by(desc + "end_date")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "status":
            jobs = Job.objects.order_by(desc + "status")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        else:
            return Response(
                f"Error: Sort term={attribute} is not found",
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["GET"])
def job_list_search(request, items_per_page, page, search):
    """
    Handle searching for a job venue or region

    - GET: Return a list of all jobs with matching search term
    """

    if request.method == "GET":
        end_index = page * items_per_page
        start_index = end_index - items_per_page

        num_result = Job.objects.filter(
            Q(j_client__region__icontains=search)
            | Q(j_client__venue_name__icontains=search)
        ).count()
        jobs = Job.objects.filter(
            Q(j_client__region__icontains=search)
            | Q(j_client__venue_name__icontains=search)
        )[start_index:end_index]
        serializer = JobSerializer(jobs, many=True)
        return JsonResponse(
            {
                "total_num_pages": math.ceil(num_result / items_per_page),
                "jobs": serializer.data,
            }
        )


@api_view(["GET"])
def job_list_search_sort(request, items_per_page, page, search, attribute, order):
    """
    Handle searching for a job venue or region

    - GET: Return a list of all jobs with matching search term
    """

    if order == "ASC":
        desc = ""
    elif order == "DSC":
        desc = "-"

    if request.method == "GET":
        end_index = page * items_per_page
        start_index = end_index - items_per_page

        if order == "ASC":
            desc = ""
        elif order == "DSC":
            desc = "-"

        jobs = Job.objects.filter(
            Q(j_client__region__icontains=search)
            | Q(j_client__venue_name__icontains=search)
        )[start_index:end_index]

        num_result = Job.objects.filter(
            Q(j_client__region__icontains=search)
            | Q(j_client__venue_name__icontains=search)
        ).count()

        if attribute == "region":
            jobs = Job.objects.filter(
                Q(j_client__region__icontains=search)
                | Q(j_client__venue_name__icontains=search)
            ).order_by(desc + "j_client__region")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "venue_name":
            jobs = Job.objects.filter(
                Q(j_client__region__icontains=search)
                | Q(j_client__venue_name__icontains=search)
            ).order_by(desc + "j_client__venue_name")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "start_date":
            jobs = Job.objects.filter(
                Q(j_client__region__icontains=search)
                | Q(j_client__venue_name__icontains=search)
            ).order_by(desc + "start_date")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "end_date":
            jobs = Job.objects.filter(
                Q(j_client__region__icontains=search)
                | Q(j_client__venue_name__icontains=search)
            ).order_by(desc + "end_date")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        elif attribute == "status":
            jobs = Job.objects.filter(
                Q(j_client__region__icontains=search)
                | Q(j_client__venue_name__icontains=search)
            ).order_by(desc + "status")[start_index:end_index]
            serializer = JobSerializer(jobs, many=True)
            return JsonResponse(
                {
                    "total_num_pages": math.ceil(num_result / items_per_page),
                    "jobs": serializer.data,
                }
            )
        else:
            return Response(
                f"Error: Sort term={attribute} is not found",
                status=status.HTTP_404_NOT_FOUND,
            )


@api_view(["POST", "PATCH"])
@permission_classes([RoleBasedPermission])
def job_add(request):
    """
    Handle operations on a single job.

    - GET: Return details of a specific job.
    - PUT: Update details of a specific job.
    - DELETE: Remove a specific job from the system.
    """

    if request.method == "POST":
        try:
            data = request.data
            venue_name = data.get("venue_name")
            j_client = Client.objects.get(venue_name=venue_name)
            start_date = data.get("start_date")
            start_date = datetime.date(*map(int, start_date.split("-")))
            end_date = data.get("end_date")
            end_date = datetime.date(*map(int, end_date.split("-")))
            marking_days = (end_date - start_date).days
            status = data.get("status")
            job = Job(
                j_client=j_client,
                start_date=start_date,
                end_date=end_date,
                marking_days=marking_days,
                status=status,
            )
            job.save()
            create_performance(job)
        except Exception as e:
            return JsonResponse({"error": f"Failed to add job. {e}"}, status=400)
        return JsonResponse({"success": f"Job created successfully."}, status=201)

    elif request.method == "PATCH":
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_performance(serializer.data["id"])
            print("update performancce")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([RoleBasedPermission])
def job_delete(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return Response(
            f"Error: Job id={job_id} is not found", status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "DELETE":
        job.delete()
        return Response("Delete Successfully", status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PATCH"])
@permission_classes([RoleBasedPermission])
def job_basic_detail(request, job_id):
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return Response(
            f"Error: Job id={job_id} is not found", status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = JobSerializer(job)
        return Response(serializer.data)

    elif request.method == "PATCH":
        try:
            data = request.data
            job_instance = Job.objects.get(pk=job_id)
            serializer = JobSerializer(job_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                update_performance(job_id)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Job.DoesNotExist:

            return Response(
                f"Error: Job id={job_id} is not found", status=status.HTTP_404_NOT_FOUND
            )


@csrf_exempt
@api_view(["GET", "POST", "PATCH"])
@permission_classes([RoleBasedPermission])
def markingJob_list(request, job_id):
    """
    Handle listing all marking jobs for a specific job or adding a new marking job.

    - GET: Return a list of marking jobs for a specified job.
    - POST: Add a new marking job for a specific job.
    - PATCH: Partially update a list of marking jobs for a specific job.
    """
    if request.method == "GET":
        markingJob = MarkingJob.objects.filter(mj_job=job_id)
        serializer = MarkingJobSerializer(markingJob, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        data["mj_job"] = job_id

        serializer = MarkingJobSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            calculate_performance(job_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        # Expect a list of marking jobs to be updated
        marking_jobs_data = request.data
        response_data = []
        errors = []

        for mj_data in marking_jobs_data:
            try:
                markingJob_instance = MarkingJob.objects.get(id=mj_data["id"])
                serializer = MarkingJobSerializer(
                    markingJob_instance, data=mj_data, partial=True
                )  # partial=True allows partial updates

                if serializer.is_valid():
                    serializer.save()
                    response_data.append(serializer.data)
                else:
                    errors.append(serializer.errors)
            except MarkingJob.DoesNotExist:
                errors.append({"id": mj_data["id"], "error": "MarkingJob not found"})

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        calculate_performance(job_id)
        return Response(response_data, status=status.HTTP_200_OK)


def update_performance(job_id):
    calculate_performance(job_id)


@csrf_exempt
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([RoleBasedPermission])
def markingJob_detail(request, markingJob_id, job_id):
    """
    Handle operations on a single marking job.

    - GET: Return details of a specific marking job.
    - PATCH: Partially update a specific marking job.
    - DELETE: Remove a specific marking job from the system.
    """
    try:
        markingJob = MarkingJob.objects.get(pk=markingJob_id, mj_job=job_id)
    except MarkingJob.DoesNotExist:
        return Response(
            f"Error: MarkingJob id={markingJob_id} is not found",
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        serializer = MarkingJobSerializer(markingJob)
        return Response(serializer.data)

    elif request.method == "PATCH":
        # Data to be updated
        data_to_update = {
            "fin_corners": request.data.get("fin_corners", markingJob.fin_corners),
            "fin_numbers": request.data.get("fin_numbers", markingJob.fin_numbers),
            "fin_others": request.data.get("fin_others", markingJob.fin_others),
        }

        # Preliminary data
        pre_data = {
            "pre_corners": markingJob.pre_corners,
            "pre_numbers": markingJob.pre_numbers,
            "pre_others": markingJob.pre_others,
        }

        # Mapping to know which 'final' corresponds to which 'preliminary'
        mapping = {
            "fin_corners": "pre_corners",
            "fin_numbers": "pre_numbers",
            "fin_others": "pre_others",
        }

        # Compare the updated data with the preliminary data
        for fin_key, pre_key in mapping.items():
            updated_value = data_to_update[fin_key]
            initial_value = pre_data[pre_key]

            if (
                    updated_value is not None
                    and initial_value is not None
                    and updated_value > initial_value
            ):
                return Response(
                    f"Error: The final value {updated_value} for {fin_key} must not be greater than the preliminary value {initial_value}",
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = MarkingJobSerializer(markingJob, data=data_to_update, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    elif request.method == "DELETE":
        markingJob.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(["GET", "PUT"])
@permission_classes([RoleBasedPermission])
def performance_detail(request, job_id):
    """
    Handle operations on the performance detail of a specific job.

    - GET: Return the performance details of a specific job.
    - PATCH: Partially update the performance details of a specific job.
    """
    try:
        job = Job.objects.get(pk=job_id)
    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    performance = job.performance
    if request.method == "GET":
        serializer = PerformanceSerializer(performance)
        return Response(serializer.data)


def create_performance(job):
    performance = Performance(p_job=job)
    performance.save()


def calculate_performance(job_id):
    try:
        job = Job.objects.get(id=job_id)
    except ObjectDoesNotExist:
        print(f"Error: Job with ID {job_id} does not exist.")
        return
    except DatabaseError as e:
        print(f"Database Error: {e}")
        return
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return

    try:
        days = job.marking_days

        marking_jobs = MarkingJob.objects.filter(mj_job=job_id)
        total_marks = sum(
            mj.fin_corners + mj.fin_numbers + mj.fin_others for mj in marking_jobs
        )
        halls = {mj.mj_hall for mj in marking_jobs}

        employees = Employee.objects.filter(e_job=job_id)
        fte_days = sum(e.days for e in employees if e.type == "Full-time-employee")
        helper_days = sum(e.days for e in employees if e.type == "Helper")

        if fte_days + helper_days == 0:
            print("Error: No employee days recorded.")
            return

        performance = Performance.objects.get(p_job=job_id)

        performance.total_marks = total_marks
        performance.total_halls = len(halls)
        performance.marks_day = round(total_marks / days, 2)
        performance.marks_fte_day = round(total_marks / fte_days, 2) if fte_days else 0
        performance.marks_person_day = round(total_marks / (fte_days + helper_days), 2)
        performance.marks_window = days
        performance.marks_hall = round(total_marks / len(halls), 2) if halls else 0
        performance.halls_day = round(len(halls) / days, 2)
        performance.fte = sum(1 for e in employees if e.type == "Full-time-employee")
        performance.intern_helper = sum(1 for e in employees if e.type == "Helper")
        performance.fte_engineer_days = fte_days
        performance.intern_helper_days = helper_days
        performance.fte_ratio = round(fte_days / (fte_days + helper_days), 2) if (fte_days + helper_days) else 0

        performance.save()

    except ZeroDivisionError as e:
        print(f"Division by Zero Error: {e}")
    except DatabaseError as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")



@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([RoleBasedPermission])
def hall_list(request, client_id):
    """
    Handle listing all halls for a specific client or adding a new hall for them.

    - GET: Return a list of all halls for a specific client.
    - POST: Add a new hall for a specified client.
    """
    if request.method == "GET":
        halls = Hall.objects.filter(h_client=client_id)
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        client = Client.objects.get(pk=client_id)
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(h_client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes([RoleBasedPermission])
def hall_list_by_job(request, job_id):
    """
    Handle listing all halls for a specific job or adding a new hall for them.

    - GET: Return a list of all halls for a specific job.
    - POST: Add a new hall for a specified job.
    """
    if request.method == "GET":
        job = Job.objects.get(pk=job_id)
        client_id = job.j_client.id
        halls = Hall.objects.filter(h_client=client_id)
        serializer = HallSerializer(halls, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        job = Job.objects.get(pk=job_id)
        client_id = job.j_client.id
        client = Client.objects.get(pk=client_id)
        serializer = HallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(h_client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["GET", "DELETE", "PATCH"])
@permission_classes([RoleBasedPermission])
def hall_detail(request, hall_id):
    """
    Handle operations on a single hall.

    - GET: Return details of a specific hall.
    - DELETE: Remove a specific hall from the system.
    - PATCH: Partially update details of a specific hall.
    """
    try:
        hall = Hall.objects.get(pk=hall_id)

    except Hall.DoesNotExist:  # change Client.DoesNotExist to Hall.DoesNotExist
        return Response({"error": "Hall not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = HallSerializer(hall)
        return Response(serializer.data)

    elif request.method == "DELETE":
        hall.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PATCH":
        serializer = HallSerializer(hall, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def job_general_info(request, job_id):
    """
    Handles getting job general information and adding employees for a given job id.

    - GET: Returns general job info including a list of employees given a marking job.
    - POST: Updates the employees section given a list of employees.
    """

    # Find job.
    try:
        calculate_performance(job_id)
        job = Job.objects.get(pk=job_id)

    except Job.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # Find employees.
        employees = Employee.objects.filter(e_job=job_id)
        serializer = EmployeeSerializer(employees, many=True)
        # Format and return.
        return JsonResponse(
            {
                "start_date": job.start_date,
                "end_date": job.end_date,
                "status": job.status,
                "employees": list(serializer.data),
            },
            safe=False,
            status=200,
        )

    elif request.method == "POST":
        errors = []
        try:
            data = json.loads(request.body)
            employees_data = data.get("employees", [])

            if not employees_data:
                raise ValueError("No employee data provided.")

            for employee_data in employees_data:
                employee_data["e_job"] = job_id
                employee_id = employee_data.get("id")

                if employee_id:
                    try:
                        # If ID exists, update the existing employee
                        employee = Employee.objects.get(id=employee_id, e_job=job_id)
                        serializer = EmployeeSerializer(
                            employee, data=employee_data, partial=True
                        )

                    except Employee.DoesNotExist:
                        errors.append(f"Employee with ID {employee_id} does not exist.")
                        continue

                else:
                    # If ID does not exist, create a new employee
                    serializer = EmployeeSerializer(data=employee_data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    update_performance(job_id)

                else:
                    errors.append(serializer.errors)

            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"success": "Employees updated successfully."},
                status=status.HTTP_200_OK,
            )

        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def job_general_info_marking_day(request, job_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            marking_days = data.get('total_mark_day')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Malformed JSON'}, status=400)
        try:
            job = Job.objects.get(id=job_id)
            job.marking_days = marking_days
            job.save()
            return Response({"success": "Total marking days updated successfully."})
        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def job_summary(request, job_id):
    """
    Handles getting job summary for a given job id.

    - GET: Returns job summary.

    """

    # Find job.
    try:
        job = Job.objects.get(pk=job_id)

    except:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # Find employees.
        job_serializer = JobSerializer(job)
        client_serializer = ClientSerializer(job.j_client)
        performance_details = PerformanceSerializer(job.performance)
        # markingJobs = MarkingJob.objects.filter(mj_job=job_id)
        # markingJob_details = MarkingJobSerializer(markingJobs, many=True)

        # Format and return.
        return JsonResponse(
            {
                "job": job_serializer.data,
                "client": client_serializer.data,
                "performance": performance_details.data,
            },
            status=200,
        )
