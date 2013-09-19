from prelabq.models import PrelabQuiz, QuizItems
usr = PrelabQuiz.objects.create(quizName='Safety Pre-Lab Quiz',courseNum='')
usr = PrelabQuiz.objects.create(quizName='Introductory Laboratory Techniques Pre-lab Quiz',courseNum='2a')
usr = PrelabQuiz.objects.create(quizName='Observing Chemical Reactions',courseNum='2a')
usr = PrelabQuiz.objects.create(quizName='Reactions of Copper',courseNum='2a')
usr = PrelabQuiz.objects.create(quizName='Volumetric Analysis',courseNum='2a')
usr = PrelabQuiz.objects.create(quizName='Spectroscopic Analysis of Mixture',courseNum='2a')
usr = PrelabQuiz.objects.create(quizName='Determining Avogadro\'s Number',courseNum='2a')

quiz = PrelabQuiz.objects.get(quizName__regex=r'^Safety')
usr = quiz.quizitems_set.create(question="After you have completed the experimental procedures you may remove your goggles only when",
        choices=["a. all the students have finished their experiment and put away any glassware.", "b. you finished the experiment.", "c. another person finished the experiment."],
        answer=0)
usr = quiz.quizitems_set.create(question="What to do if you spill chemical on your hand",
        choices=["a. wipe it out with paper towel", "b. wash with copious of water for 15 minutes", "c. put some sodium bicarbonate on your hand"],
        answer=1)
usr = quiz.quizitems_set.create(question="Which of the following apparel is allowed in the lab",
        choices=["a. Open-toed shoes", "b. long leggings", "c. closed-toed, closed-healed, long sleeves"],
        answer=2)
usr = quiz.quizitems_set.create(question="If the fire alarm is on, what is the following action is correct",
        choices=["a. run out of the lab room immediately", "b. continue the lab regardless of what TA asks to do", "c. evacuate the building following the guidance of TA"],
        answer=2)

quiz = PrelabQuiz.objects.get(quizName__regex=r'^Intro')
usr = quiz.quizitems_set.create(question="What tool should you use to handle the hot crucible after heating it on the wire triangle?",
        choices=["a. Your bare hands", "b. Paper towels.", "c. Crucible tongs without the rubber-ended tips"],
        answer=2)
usr = quiz.quizitems_set.create(question="In part B of this lab, which of the following pieces of glassware is used to accurately transfer 24.00 mL of water",
        choices=["a. Graduated Cylinder", "b. Buret", "c. Disposable Pipet"],
        answer=1)
usr = quiz.quizitems_set.create(question="When finished with solid, dry manganess(II) monohydrate, you must",
        choices=["a. Dump it in the trashcan.", "b. Pour it down the drain with copious amounts of water.", "c. Dispose of it by placing it into the proper container found in the fumehood"],
        answer=2)

quiz = PrelabQuiz.objects.get(quizName__regex=r'^Observ')
usr = quiz.quizitems_set.create(question="Question a",
        choices=["a. a-1", "b. a-2", "c. a-3"],
        answer=2)
usr = quiz.quizitems_set.create(question="Question b",
        choices=["a. b-1", "b. b-2", "c. b-3"],
        answer=2)
usr = quiz.quizitems_set.create(question="Question c",
        choices=["a. c-1", "b. c-2", "c. c-3"],
        answer=2)

