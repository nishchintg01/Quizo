from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login,logout
from .models import *
from django.db.models import Q


# Intro Page
def Login(request):
	return render(request,'loginSignup.html')

# Logout Url
@login_required
def Logout(request):
	logout(request)
	return redirect('login')

# User Dashboard
@login_required
def UserDashboard(request):
	context = {}
	if request.user.is_staff:
		Quizes = Quiz.objects.filter(user=request.user)
		context['users'] = Quizes
		context['logggedin'] = 'teacher'
	else:
		context['users'] = Quiz.objects.all()
		context['logggedin'] = 'student'

	if request.method == "POST":
		title = request.POST.get("title")
		if title:
			data = Quiz(
				Title = title,
				user = request.user
			).save()
	request.session["start"] = 1
	return render(request,'dashboard.html',context)


# Login APIs
@csrf_exempt
def LoginAPI(request):
	data = {}
	if request.method == 'POST':
		email = request.POST.get("loginusername","")
		password = request.POST.get("loginpassword","")
		user = authenticate(username=email, password=password) # Authenticate if credentials are correct
		print(user)
		if user is not None: # Check if your exists
			login(request,user)
			return redirect("dashboard")
		else:
			data["error"] = "User Does Not Exists! Sign Up "
			return render(request,'loginSignup.html',data)
	return redirect("login")


# Singup APIs For Creation of Different Type of Users
@csrf_exempt
def SignupAPI(request):
	data = {}
	if request.is_ajax():
		username = request.POST.get("username")
		email = request.POST.get("email")
		password = request.POST.get("password")
		usertype = request.POST.get("exampleRadios")
		print(password)
		print(username)
		# Check if Username or email already Exists in Database
		if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
			data["is_taken"] = "User Already Exists"
			return JsonResponse(data,safe=False)
		else:
			user = User.objects.create(username=username, email=email)
			if usertype=="teacher":
				user.is_staff = True
				user.set_password(password)
				user.save()
			else:
				user.set_password(password)
				user.save()
			data['sucess']= True
	return JsonResponse(data,safe=False)

# Delete Quiz
@login_required
def DeleteQuiz(request,pk):
	try:
		data = Quiz.objects.get(id=pk)
		data.delete()
	except:
		print("Object Does Not Exists")
	return redirect("dashboard")


# Add Questions to the Quiz
@login_required
def AddQuestions(request,pk):
	quiz = Quiz.objects.get(id=pk)
	if quiz.test.all().count() == 10:
		return redirect("dashboard")
	if request.method == "POST":
		context = {}
		print(request.POST)
		question = request.POST.get("question title")
		option = request.POST.getlist("options")
		explain = request.POST.get("explain")
		correct_ans1 = request.POST.get("correct1")
		correct_ans2 = request.POST.get("correct2")
		correct_ans3 = request.POST.get("correct3")
		correct_ans4 = request.POST.get("correct4")
		correct = (correct_ans1, correct_ans2 , correct_ans3 ,correct_ans4 )
		correct = ','.join(filter(None, correct))
		if correct:
			data = Questions(
				quiz = quiz,
				Title = question,
				Option1 = option[0],
				Option2 = option[1],
				Option3 = option[2],
				Option4 =  option[3],
				Explaination = explain,
			)
			data.Correct_answer = correct
			if len(correct)>1:
				data.Single_Answer = False
				data.save()
			data.save()
			return render(request,"AddQuestions.html",context)
		else:
			print("error")
			context["errors"] = "Correct answer must be Selected"
			return render(request,"AddQuestions.html",context)
	return render(request,"AddQuestions.html")


# Begin Quiz
@login_required
def BeginQuiz(request,pk):
	quiz = Quiz.objects.get(id=pk)
	count = quiz.test.all().count()
	request.session["time"] = 10
	request.session["quiz"] = pk
	request.session["count"] = count
	question = quiz.test.all()
	if question:
		context = {
            'quiz':quiz,
            'question':question[request.session["start"]-1],
            'last':count,
            'start': request.session["start"],
            'time':request.session["time"]
            }
		return render(request,"quiz.html",context)
	else:
		return redirect("dashboard")



# API to check if the answer is correct or not
@csrf_exempt
def CheckAnswer(request):
	request.session["status"]= "Not submitted"
	data = {}
	if request.is_ajax():
		answer = request.POST.get("value")
		time = request.POST.get("time")
		request.session["time"] = time
		pk = request.POST.get("question")
		print(answer)
		try:
			question = Questions.objects.get(id=pk)
			if answer in question.Correct_answer:
				data["success"] = "asas"
			else:
				data["error"] = "asas"
			ans = Answers(
				user = request.user,
				quiz = Quiz.objects.get(id=request.session["quiz"]),
				question = question.Title,
				option1 = question.Option1,
				option2 = question.Option2,
				option3 = question.Option3,
				option4 = question.Option4,
				answer = answer,
				correct = question.Correct_answer,
				time_taken = time,
				explaination = question.Explaination
			)
			ans.save()
			print(ans)
			if request.session["start"] == request.session["count"]:
				quiz = Quiz.objects.get(Q(id=request.session["quiz"]) and Q(user=request.user))
				quiz.Attempted = True
				quiz.save()
			request.session["start"] +=1
		except:
			data["error"] = "asas"
	return JsonResponse(data,safe=False)


# Quiz Result
@login_required
def ResultQuiz(request,pk):
	quiz = Quiz.objects.get(id=pk)
	answers = Answers.objects.filter(Q(user=request.user)&Q(quiz=quiz))
	attemptes_questions = answers.count()
	correct = 0
	for ans in answers:
		print(ans.correct,ans.answer)
		if ans.answer == ans.correct:
			correct +=1
	time = 0
	for ans in answers:
		time += 60 - ans.time_taken
	if time>60:
		minutes = time //60
		seconds = time % 60
		time_taken = f"{minutes} minutes {seconds} seconds "
	else:
		time_taken = f"{time} seconds "
	context = {
		'attempted':attemptes_questions,
		'correct':correct,
		'time':time_taken
	}
	return render(request,"result.html",context)

# Detailed report of student
def detailedreport(request,pk):
	quiz = Quiz.objects.get(id=pk)
	answers = Answers.objects.filter(Q(user=request.user)&Q(quiz=quiz))
	context = {
		'answers':answers,
	}
	return render(request,"report.html",context)