from django.db import models
from django.contrib.auth.models import User


class Kit(models.Model):
    name = models.CharField(max_length=75, unique=True)

    def __str__(self):
        return self.name

    def getSections(self):
        return Section.objects.filter(kit=self).order_by('section_number')

    def getConfirmedSections(self):
        return Section.objects.filter(kit=self, confirmed=True).order_by('section_number')

    def getCleanedName(self):
        return self.name.replace(' ', '-').replace('/', '-')


class Section(models.Model):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, null=False)
    section_number = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=75)
    confirmed = models.BooleanField(default=True)

    def __str__(self):
        return "Section %s: %s" % (str(self.section_number), self.name)

    def getPages(self):
        return Page.objects.filter(section=self).order_by('page_number')

    def getConfirmedPages(self):
        return Page.objects.filter(section=self, confirmed=True).order_by('page_number')


class Page(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    page_number = models.CharField(max_length=2)
    confirmed = models.BooleanField(default=True)

    def __str__(self):
        return "%s-%s" % (str(self.section.section_number), str(self.page_number))

    def getSteps(self):
        return Step.objects.filter(page=self).order_by('step_number')

    def getConfirmedSteps(self):
        return Step.objects.filter(page=self, confirmed=True).order_by('step_number')

    def getCompletionStatus(self):
        verified = Step.objects.filter(page=self, status='V').count()
        total = self.getSteps().count()
        return "%s/%s Steps Verified" % (verified, total)


class Step(models.Model):
    STATUS_CHOICES = (
        ('I', 'Incomplete'),
        ('S', 'Started'),
        ('B', 'Blocked'),
        ('C', 'Completed'),
        ('V', 'Verified'),
    )
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField()
    step_text = models.TextField()
    confirmed = models.BooleanField(default=True)
    date_completed = models.DateField(null=True, blank=True)
    date_verified = models.DateField(null=True, blank=True)

    # user_completed
    # mentor_verified

    # Step status can be accessed by get_status_display()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='I')

    def __str__(self):
        return "Step " + str(self.step_number)

    def getNotes(self):
        return Step_Note.objects.filter(step=self).order_by('date_created')

    def getStatusStyle(self):
        if self.status is 'I':
            return ''
        elif self.status is 'S':
            return 'active'
        elif self.status is 'B':
            return 'danger'
        elif self.status is 'C':
            # 'info' is not working for some reason?
            return 'warning'
        elif self.status is 'V':
            return 'success'

    def getStatus(self):
        if self.status is 'I':
            return 'Incomplete'
        elif self.status is 'S':
            return 'Started'
        elif self.status is 'B':
            return 'Blocked'
        elif self.status is 'C':
            return 'Completed'
        elif self.status is 'V':
            return 'Verified'


class Step_Note(models.Model):
    step = models.ForeignKey(Step)
    user = models.ForeignKey(User, editable=False)
    text = models.TextField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "[%s] %s: %s" % (self.date_created, self.user.username, self.text)
