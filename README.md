This side project provides a prototype of an online interface for students' to complete postlab homework and evaluate their results using Django web framework and MySQL with postlab contents initially in xls format. 
So far, the functionalities provided are users' login and sample prelab and postlab interactions and evaluations.

login: -- login and authentication component
	models.py -- models classes
	views.py -- display the login page
prelabq: -- prelab component
	models.py -- model classes
	views.py -- display the login page
	prelabform.py -- generate prelab question form for display
postlabq: -- postlab component
	models.py -- model classes
	views.py -- display the login page
	xlsinput.py -- retrive information from spreadsheet
	specquiz.py -- code for initial build of database of questions
	basicinput.py -- some test codes for question name input
	eqeval.py -- equation evaluation 
mytemplates: -- all the static html templates and css files for rendering
