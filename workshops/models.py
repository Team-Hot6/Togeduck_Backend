from django.db import models
from users.models import User


class Hobby(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return str(self.category)


class Location(models.Model):
    district = models.CharField(max_length=20)

    def __str__(self):
        return str(self.district)


class Workshop(models.Model):
    category = models.ForeignKey(Hobby, on_delete=models.CASCADE, related_name='workshop_category')
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workshop_host')
    date = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    address = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=500)
    workshop_image = models.ImageField(upload_to='workshop/')
    max_guest = models.IntegerField()
    amount = models.DecimalField(decimal_places=0, max_digits=10000000000000000)
    created_at = models.DateTimeField(auto_now_add=True)
    participant = models.ManyToManyField(User, related_name='workshop_participant', blank=True, through='WorkshopApply', through_fields=('workshop', 'guest'),) 
    likes = models.ManyToManyField(User, related_name='workshop_likes', blank=True)

    def __str__(self):
        return self.title 



class WorkshopApply(models.Model):
    CHOISE_TYPE = (
    ('승인', '승인'),
    ('거절', '거절'),
    ('대기', '대기'))
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE) 
    result = models.CharField("신청 유형", choices=CHOISE_TYPE, null=True, max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "workshop_apply"

CHOISE_TYPE = (
    ('승인', '승인'),
    ('거절', '거절'),
    ('대기', '대기'))

class WorkshopApply(models.Model): # 워크샵 신청 중간 테이블
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE) # 참가하려는 특정 워크샵
    guest = models.ForeignKey(User, on_delete=models.CASCADE) # 참가 신청자
    result = models.CharField("신청 유형", choices=CHOISE_TYPE, null=True, max_length=3) # 신청에 대한 승낙/거절 여부
    created_at = models.DateTimeField(auto_now_add=True) # 참가신청 시간

    class Meta:
        db_table = "workshop_apply"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reveiw_user')
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name='review_workshop')
    content = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)




