from django.test import TestCase
from .models import *
from django.contrib.auth.models import User


# Basic test Case for Models: Quiz, Question, Answers
class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="nishchint",email="nish@gmail.com")
        self.user.set_password = "ng01011999"
        self.user = self.user.save()

    def test_quiz(self):
        quiz = Quiz()
        quiz.user = User.objects.get(id=1)
        quiz.Title = "testing Quiz"
        quiz.save()
        print("Quiz Created")
        record = Quiz.objects.get(id=1)
        self.assertEquals(record,quiz)
        print("Test Successfull")

    def test_questions(self):
        quiz = Quiz()
        quiz.user = User.objects.get(id=1)
        quiz.Title = "testing Quiz"
        quiz.save()
        print("\nQuiz Created")
        question = Questions()
        question.quiz = Quiz.objects.get(id=1)
        question.Title ="Test Question"
        question.Option1 = "test1"
        question.Option2 = "test2"
        question.Option3 = "test3"
        question.Option4 = "test4"
        question.Single_Answer = True
        question.Correct_answer = "2"
        question.Explaination ="Test Explanation"
        question.save()
        record = Questions.objects.get(id=1)
        self.assertEquals(record,question)
        print("Test Question Successfull")

    def test_answers(self):
        quiz = Quiz()
        quiz.user = User.objects.get(id=1)
        quiz.Title = "testing Quiz"
        quiz.save()
        print("\nQuiz Created")
        question = Questions()
        question.quiz = Quiz.objects.get(id=1)
        question.Title ="Test Question"
        question.Option1 = "test1"
        question.Option2 = "test2"
        question.Option3 = "test3"
        question.Option4 = "test4"
        question.Single_Answer = True
        question.Correct_answer = "2"
        question.Explaination ="Test Explanation"
        question.save()
        ans = Answers()
        ans.user = User.objects.get(id=1)
        ans.quiz = quiz
        ans.question = question.Title
        ans.option1 = question.Option1
        ans.option2 = question.Option2
        ans.option3 = question.Option3
        ans.option4 = question.Option4
        ans.question = question.Title
        ans.answer = "1"
        ans.correct = "2"
        ans.time_taken = 30
        ans.Explaination = question.Explaination
        ans.save()
        record = Answers.objects.get(id=1)
        self.assertEquals(record,ans)
        print("Test Answer Successfull")
