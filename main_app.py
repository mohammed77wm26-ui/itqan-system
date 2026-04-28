from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):
    STAGES = [
        ('ابتدائي', 'ابتدائي'), ('متوسط', 'متوسط'), 
        ('ثانوي', 'ثانوي'), ('جامعي', 'جامعي')
    ]
    name = models.CharField(max_length=255, verbose_name="الاسم الثلاثي")
    age = models.IntegerField(verbose_name="العمر")
    stage = models.CharField(max_length=50, choices=STAGES, verbose_name="المرحلة")
    student_id = models.CharField(max_length=20, unique=True, verbose_name="الرقم التسلسلي")
    phone = models.CharField(max_length=15, verbose_name="الهاتف")
    
    def __str__(self):
        return self.name

class Grade(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    quran = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    fiqh = models.FloatField()
    hadith = models.FloatField()
    seerah = models.FloatField()
    
    @property
    def final_avg(self):
        # تطبيق معادلتك الاحترافية: 50% قرآن و 50% باقي المواد
        others = (self.fiqh + self.hadith + self.seerah) / 3
        return round((self.quran * 0.5) + (others * 0.5), 2)

