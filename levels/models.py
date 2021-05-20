from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    Title = models.CharField(max_length=2000)
    user = models.ForeignKey(User,related_name="user",on_delete=models.CASCADE)
    Attempted = models.BooleanField(default=False)

    def __str__(self):
        return self.Title

class Questions(models.Model):
    quiz = models.ForeignKey(Quiz,related_name="test",on_delete=models.CASCADE)
    Title = models.CharField(max_length = 8000)
    Option1 = models.CharField(max_length = 2000)
    Option2 = models.CharField(max_length = 2000)
    Option3 = models.CharField(max_length = 2000)
    Option4 = models.CharField(max_length = 2000)
    Single_Answer = models.BooleanField(default=True)
    Correct_answer = models.TextField()
    Explaination = models.TextField()
    
    def __str__(self):
        return self.Title

class Answers(models.Model):
    user = models.ForeignKey(User,related_name="student",on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz,related_name="answer",on_delete=models.CASCADE)
    question = models.CharField(max_length = 8000)
    option1 = models.CharField(max_length = 2000)
    option2 = models.CharField(max_length = 2000)
    option3 = models.CharField(max_length = 2000)
    option4 = models.CharField(max_length = 2000)
    answer = models.TextField()
    correct = models.TextField()
    time_taken = models.IntegerField(default=0)
    explaination = models.TextField()

    def __str__(self):
        return self.question