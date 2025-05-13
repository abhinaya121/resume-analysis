from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
	       path('AdminLogin.html', views.AdminLogin, name="AdminLogin"), 
	       path('AdminLoginAction.html', views.AdminLoginAction, name="AdminLoginAction"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path('UserLoginAction', views.UserLoginAction, name="UserLoginAction"),	   
	       path('Signup', views.Signup, name="Signup"),
	       path('SignupAction', views.SignupAction, name="SignupAction"),
	       path('PostJobs', views.PostJobs, name="PostJobs"),
	       path('PostJobsAction', views.PostJobsAction, name="PostJobsAction"),
	       path('ViewScore', views.ViewScore, name="ViewScore"),
	       path('Feedback', views.Feedback, name="Feedback"),
	       path('FeedbackAction', views.FeedbackAction, name="FeedbackAction"),	
	       path('Aboutus', views.Aboutus, name="Aboutus"),
	       path('ViewFeedback', views.ViewFeedback, name="ViewFeedback"),
	       path('ViewJobs', views.ViewJobs, name="ViewJobs"),
	       path('UploadResume', views.UploadResume, name="UploadResume"),
	       path('UploadResumeAction', views.UploadResumeAction, name="UploadResumeAction"),	   
	       path('ViewScore', views.ViewScore, name="ViewScore"),
]