import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basescrip_backend.settings')
django.setup()

from core.models import Activity, Question, AnswerOption

def populate():
    print("Starting database population of extra questions...")

    # Fetch activities
    try:
        activity2 = Activity.objects.get(pk=2)
        print(f"Found Activity 2: {activity2.title}")
    except Activity.DoesNotExist:
        print("Activity 2 not found. Make sure sample_levels fixture is loaded.")
        return

    try:
        activity3 = Activity.objects.get(pk=3)
        print(f"Found Activity 3: {activity3.title}")
    except Activity.DoesNotExist:
        print("Activity 3 not found. Make sure sample_levels fixture is loaded.")
        return

    try:
        activity4 = Activity.objects.get(pk=4)
        print(f"Found Activity 4: {activity4.title}")
    except Activity.DoesNotExist:
        print("Activity 4 not found. Make sure sample_levels fixture is loaded.")
        return

    # Questions for Activity 2: Grammar: Mission 1 - Sentence Launch (Scrambled Sentence)
    q2_1, created = Question.objects.get_or_create(
        activity=activity2,
        text="Arrange the words to form a correct sentence: is / 13 / Leo / old / years / .",
        is_free_text=False
    )
    if created:
        AnswerOption.objects.create(question=q2_1, text="Leo is 13 years old.", is_correct=True)
        print("Created Question 1 for Activity 2")

    q2_2, created = Question.objects.get_or_create(
        activity=activity2,
        text="Arrange the words to form a correct sentence: from / is / Peru / He / .",
        is_free_text=False
    )
    if created:
        AnswerOption.objects.create(question=q2_2, text="He is from Peru.", is_correct=True)
        print("Created Question 2 for Activity 2")

    # Questions for Activity 3: Mission 2: Word Recovery Zone (Fill in the Blanks)
    q3_1, created = Question.objects.get_or_create(
        activity=activity3,
        text="He ___ from Peru and he ___ 13 years old.",
        is_free_text=False
    )
    if created:
        AnswerOption.objects.create(question=q3_1, text="is / is", is_correct=True)
        AnswerOption.objects.create(question=q3_1, text="am / is", is_correct=False)
        AnswerOption.objects.create(question=q3_1, text="are / am", is_correct=False)
        print("Created Question 1 for Activity 3")

    q3_2, created = Question.objects.get_or_create(
        activity=activity3,
        text="I ___ use computers and I ___ like reading.",
        is_free_text=False
    )
    if created:
        AnswerOption.objects.create(question=q3_2, text="can / like", is_correct=True)
        AnswerOption.objects.create(question=q3_2, text="can / likes", is_correct=False)
        AnswerOption.objects.create(question=q3_2, text="do / am", is_correct=False)
        print("Created Question 2 for Activity 3")

    # Questions for Activity 4: Mission 3: Ship Repair - Error Detection
    q4_1, created = Question.objects.get_or_create(
        activity=activity4,
        text="Find the error in the sentence: 'He can plays football.'",
        is_free_text=False
    )
    if created:
        AnswerOption.objects.create(question=q4_1, text="plays (should be 'play')", is_correct=True)
        AnswerOption.objects.create(question=q4_1, text="can (should be 'could')", is_correct=False)
        AnswerOption.objects.create(question=q4_1, text="football (should be 'soccer')", is_correct=False)
        print("Created Question 1 for Activity 4")

    q4_2, created = Question.objects.get_or_create(
        activity=activity4,
        text="Find the error in the sentence: 'They is from Peru.'",
        is_free_text=False
    )
    if created:
        AnswerOption.objects.create(question=q4_2, text="is (should be 'are')", is_correct=True)
        AnswerOption.objects.create(question=q4_2, text="from (should be 'of')", is_correct=False)
        AnswerOption.objects.create(question=q4_2, text="Peru (should be 'peruvian')", is_correct=False)
        print("Created Question 2 for Activity 4")

    print("Database population complete!")

if __name__ == '__main__':
    populate()
