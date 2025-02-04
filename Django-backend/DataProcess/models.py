from django.db import models


class Job(models.Model):
    j_client = models.ForeignKey('Client', on_delete=models.SET_NULL, blank=True, null=True, related_name='job')
    start_date = models.DateField(verbose_name='Statr Date')
    end_date = models.DateField(verbose_name='End Date')
    marking_days = models.IntegerField(verbose_name='Number of Marking Days', default=0)
    status = models.CharField(verbose_name='Status', max_length=64, default='NEW')
    show = models.CharField(verbose_name='Show', max_length=32, blank=True, null=True)

    class Meta:
        db_table = "job"

    def to_dict(self):
        return {'id': self.id,
                'venue_name': self.j_client.venue_name, 
                'show': self.show, 
                'marking_day': self.marking_days,
                'region': self.j_client.region,
                'start_date': self.start_date, 
                'end_date': self.end_date, 
                'status': self.status}


class MarkingJob(models.Model):
    mj_job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='mj')
    mj_hall = models.ForeignKey('Hall', on_delete=models.CASCADE, related_name='marking_jobs')
    colour = models.CharField(verbose_name='Colour', max_length=16, blank=True, null=True)
    pre_corners = models.IntegerField(verbose_name='Preliminary Corners', blank=True, null=True)
    pre_numbers = models.IntegerField(verbose_name='Preliminary Numbers', blank=True, null=True)
    pre_others = models.IntegerField(verbose_name='Preliminary Others', blank=True, null=True)
    pre_area = models.IntegerField(verbose_name='Preliminary Area', blank=True, null=True)
    fin_corners = models.IntegerField(verbose_name='Final Corners', blank=True, null=True)
    fin_numbers = models.IntegerField(verbose_name='Final Numbers', blank=True, null=True)
    fin_others = models.IntegerField(verbose_name='Final Others', blank=True, null=True)
    fin_area = models.IntegerField(verbose_name='Final Area', blank=True, null=True)

    class Meta:
        db_table = 'markingJob'

    def to_dict(self):
        return {'id': self.id,
                'job': self.mj_job.to_dict(),
                'hall': self.mj_hall.hall,
                'area': self.mj_hall.area,
                'show': self.mj_job.show, 'colour': self.colour,
                'pre_corners': self.pre_corners,
                'pre_numbers': self.pre_numbers,
                'pre_others': self.pre_others,
                'pre_area': self.pre_area,
                'fin_corners': self.fin_corners,
                'fin_numbers': self.fin_numbers, 
                'fin_others': self.fin_others,
                'fin_area': self.fin_area
                }


class Performance(models.Model):
    p_job = models.OneToOneField('Job', on_delete=models.CASCADE, related_name='performance', blank=True, null=True)
    total_halls = models.IntegerField(verbose_name='Number of Halls', default=0)
    total_shows = models.IntegerField(verbose_name='Total Shows', default=0)
    total_marks = models.IntegerField(verbose_name='Total Marks', default=0)
    marks_day = models.FloatField(verbose_name="Mark/Day", default=0)
    marks_fte_day = models.IntegerField(verbose_name='Mark/FTE/Day', default=0)
    marks_person_day = models.FloatField(verbose_name='Marks/Person/day', default=0)
    marks_window = models.IntegerField(verbose_name='Avg # of marks/window', default=0)
    marks_hall = models.IntegerField(verbose_name='Avg # of marks/hall', default=0)
    halls_day = models.FloatField(verbose_name='Halls/Day', default=0)
    fte = models.IntegerField(verbose_name='# FTE', default=0)
    intern_helper = models.IntegerField(verbose_name='Intern/Helper', default=0)
    fte_engineer_days = models.IntegerField(verbose_name='FTE/Engineer/Days', default=0)
    intern_helper_days = models.IntegerField(verbose_name='Intern/Helper/Days', default=0)
    fte_ratio = models.FloatField(verbose_name='FTE Ratio', default=0)

    class Meta:
        db_table = 'performance'


class Employee(models.Model):
    FULL_TIME_EMPLOYEE = 'Full-time-employee'
    HELPER = 'Helper'
    TYPE_CHOICES = [
        (FULL_TIME_EMPLOYEE, 'Full-time-employee'),
        (HELPER, 'Helper')
    ]

    name = models.CharField(verbose_name='Name', max_length=32)
    type = models.CharField(
        verbose_name='Type', 
        max_length=32, 
        choices=TYPE_CHOICES, 
        default=FULL_TIME_EMPLOYEE
    )
    days = models.IntegerField(verbose_name='Working days on-site')
    hall = models.CharField(verbose_name='Hall', max_length=32, blank=False)
    e_job = models.ForeignKey('Job', on_delete=models.CASCADE, related_name='employee', null= True, blank=True)

    class Meta:
        db_table = 'employee'


class Client(models.Model):
    venue_name = models.CharField(verbose_name='Venue Name', max_length=32, unique=True)
    region = models.CharField(verbose_name='Region', max_length=64, blank=False)
    email = models.EmailField(verbose_name='Email', max_length=64)
    phone = models.CharField(verbose_name='Phone Number', max_length=32)
    class Meta:
        db_table = 'client'

    def to_dict(self):
        return {
            'id': self.id,
            'venue_name': self.venue_name,
            'email': self.email,
            'phone': self.phone,
            'region': self.region, # fetch associated halls for the client
        }


class Hall(models.Model):
    hall = models.CharField(verbose_name='Hall', max_length=32, blank=False)
    area = models.IntegerField(verbose_name='Gross Area(sqm)', default=0)
    h_client = models.ForeignKey('Client', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'hall'

    def __str__(self):
        return self.hall

    def to_dict(self):
        return {'id': self.id, 'hall': self.hall, 'area': self.area}
