import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basescrip_backend.settings')
django.setup()

from core.models import Level, Mission, Activity, Question, AnswerOption

def populate():
    print("Starting database population for all 5 Days of curriculum...")

    # Clear existing curriculum tables to avoid duplicates and ensure consistent IDs
    Level.objects.all().delete()
    print("Cleared existing Level, Mission, Activity, Question, and AnswerOption records.")

    # List of days and curriculum content
    curriculum = [
        # ==========================================
        # DAY 1: Who are you?
        # ==========================================
        {
            "day_num": 1,
            "title": "Day 1 - Dimension 1: Who are you?",
            "desc": "Verb To Be (am, is, are), Preferences (like / favorite), Abilities (can).",
            "mission_title": "Personal Information: Present & Abilities",
            "story": "Welcome to the Crew: Today is a special day. The spaceship has arrived at Basescrib!. Before starting, the General wants to meet the new recruit. Tom is 13, peruvian, likes robots and can repair spaceships.",
            "activities": [
                {
                    "title": "Reading: Comic - Welcome to the Crew",
                    "desc": "Read the comic panels about Tom joining the crew and answer the questions.",
                    "max_score": 10,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Where has the spaceship arrived?",
                            "options": [
                                {"text": "Basescrib!", "is_correct": True},
                                {"text": "Mars", "is_correct": False},
                                {"text": "Earth", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What is the recruit's name?",
                            "options": [
                                {"text": "Tom", "is_correct": True},
                                {"text": "Leo", "is_correct": False},
                                {"text": "Emma", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Where is the recruit from?",
                            "options": [
                                {"text": "Peru", "is_correct": True},
                                {"text": "Brazil", "is_correct": False},
                                {"text": "Mexico", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does the recruit like?",
                            "options": [
                                {"text": "Robots and science", "is_correct": True},
                                {"text": "Football and music", "is_correct": False},
                                {"text": "Space guide books", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What can the recruit do?",
                            "options": [
                                {"text": "Repair spaceships", "is_correct": True},
                                {"text": "Fly a spaceship", "is_correct": False},
                                {"text": "Cook space food", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Grammar: Mission 1 - Sentence Launch",
                    "desc": "Arrange the scrambled words to form correct sentences.",
                    "max_score": 10,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Arrange the words to form a correct sentence: name / My / Noah / is",
                            "options": [{"text": "My name is Noah.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: years / old / am / fourteen / I",
                            "options": [{"text": "I am fourteen years old.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: favorite / purple / color / My / is",
                            "options": [{"text": "My favorite color is purple.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: like / I / robots / and / science",
                            "options": [{"text": "I like robots and science.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: can / repair / I / spaceships",
                            "options": [{"text": "I can repair spaceships.", "is_correct": True}]
                        }
                    ]
                },
                {
                    "title": "Mission 2: Word Recovery Zone",
                    "desc": "Select the correct option to fill the blanks in the sentence.",
                    "max_score": 8,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "My name ___ Emma.",
                            "options": [
                                {"text": "is", "is_correct": True},
                                {"text": "am", "is_correct": False},
                                {"text": "are", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I ___ twelve years old.",
                            "options": [
                                {"text": "am", "is_correct": True},
                                {"text": "is", "is_correct": False},
                                {"text": "are", "is_correct": False}
                            ]
                        },
                        {
                            "text": "My favorite color ___ green.",
                            "options": [
                                {"text": "is", "is_correct": True},
                                {"text": "am", "is_correct": False},
                                {"text": "like", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I ___ robots.",
                            "options": [
                                {"text": "like", "is_correct": True},
                                {"text": "am", "is_correct": False},
                                {"text": "is", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I ___ fly a spaceship.",
                            "options": [
                                {"text": "can", "is_correct": True},
                                {"text": "am", "is_correct": False},
                                {"text": "is", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Mission 3: Ship Repair - Error Detection",
                    "desc": "Identify the grammatical error in the system report.",
                    "max_score": 12,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Find the error in the sentence: 'My name are Lucas.'",
                            "options": [
                                {"text": "are (should be 'is')", "is_correct": True},
                                {"text": "name (should be 'names')", "is_correct": False},
                                {"text": "Lucas (should be 'lucas')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I is thirteen years old.'",
                            "options": [
                                {"text": "is (should be 'am')", "is_correct": True},
                                {"text": "old (should be 'age')", "is_correct": False},
                                {"text": "thirteen (should be '13')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'My favorite color are red.'",
                            "options": [
                                {"text": "are (should be 'is')", "is_correct": True},
                                {"text": "favorite (should be 'favorites')", "is_correct": False},
                                {"text": "red (should be 'blue')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I likes science.'",
                            "options": [
                                {"text": "likes (should be 'like')", "is_correct": True},
                                {"text": "I (should be 'he')", "is_correct": False},
                                {"text": "science (should be 'sciences')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I can repairs spaceships.'",
                            "options": [
                                {"text": "repairs (should be 'repair')", "is_correct": True},
                                {"text": "can (should be 'likes')", "is_correct": False},
                                {"text": "spaceships (should be 'spaceship')", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Writing: Personal Presentation",
                    "desc": "Introduce yourself to your new crew mates! Use the template below.",
                    "max_score": 20,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "You need a friend so introduce yourself: My name is __________. I am __________ years old. I am from __________. My favorite __________ is __________. I can __________.",
                            "is_free_text": True
                        }
                    ]
                }
            ]
        },
        # ==========================================
        # DAY 2: Inside Basescrib
        # ==========================================
        {
            "day_num": 2,
            "title": "Day 2 - Dimension 2: Inside Basescrib",
            "desc": "There is / there are, singular vs plural, article a/an.",
            "mission_title": "Exploring a New Planet",
            "story": "Exploring a new planet: The General tours the crew inside Basescrib. They find five computers in the study room, books, a robot showing photos of food, 10 stars, and a friendly alien in the garden.",
            "activities": [
                {
                    "title": "Reading: Comic - Inside Basescrib",
                    "desc": "Read the story about the tour inside Basescrib and answer the questions.",
                    "max_score": 10,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Where does the crew go today?",
                            "options": [
                                {"text": "Spaceship garden", "is_correct": True},
                                {"text": "Control room", "is_correct": False},
                                {"text": "Cafeteria", "is_correct": False}
                            ]
                        },
                        {
                            "text": "How many computers are there in the study room?",
                            "options": [
                                {"text": "Five computers", "is_correct": True},
                                {"text": "Three computers", "is_correct": False},
                                {"text": "Ten computers", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does the robot show to the crew?",
                            "options": [
                                {"text": "Five photos of food", "is_correct": True},
                                {"text": "A space guide", "is_correct": False},
                                {"text": "Ten stars", "is_correct": False}
                            ]
                        },
                        {
                            "text": "How many stars are there in the sky?",
                            "options": [
                                {"text": "10 stars", "is_correct": True},
                                {"text": "5 stars", "is_correct": False},
                                {"text": "No stars", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Who helps take care of the plants in the garden?",
                            "options": [
                                {"text": "A friendly alien", "is_correct": True},
                                {"text": "A small robot", "is_correct": False},
                                {"text": "The Trainer", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Grammar: Mission 1 - Sentence Launch",
                    "desc": "Arrange the scrambled words to form correct sentences.",
                    "max_score": 10,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Arrange the words to form a correct sentence: are / there / five computers",
                            "options": [{"text": "There are five computers.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: robot / there / a / is",
                            "options": [{"text": "There is a robot.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: books / there / are",
                            "options": [{"text": "There are books.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: there / photos / five / are",
                            "options": [{"text": "There are five photos.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: alien / friendly / a / there / is",
                            "options": [{"text": "There is a friendly alien.", "is_correct": True}]
                        }
                    ]
                },
                {
                    "title": "Mission 2: Word Recovery Zone",
                    "desc": "Select the correct combination to complete the sentence.",
                    "max_score": 8,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "___ five computers.",
                            "options": [
                                {"text": "There are", "is_correct": True},
                                {"text": "There is", "is_correct": False},
                                {"text": "Is there", "is_correct": False}
                            ]
                        },
                        {
                            "text": "___ a robot.",
                            "options": [
                                {"text": "There is", "is_correct": True},
                                {"text": "There are", "is_correct": False},
                                {"text": "Are there", "is_correct": False}
                            ]
                        },
                        {
                            "text": "___ many books.",
                            "options": [
                                {"text": "There are", "is_correct": True},
                                {"text": "There is", "is_correct": False},
                                {"text": "Is there", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Select the correct article for: ___ alien",
                            "options": [
                                {"text": "An", "is_correct": True},
                                {"text": "A", "is_correct": False},
                                {"text": "Some", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Select the correct article for: ___ robot",
                            "options": [
                                {"text": "A", "is_correct": True},
                                {"text": "An", "is_correct": False},
                                {"text": "Any", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Mission 3: Ship Repair - Error Detection",
                    "desc": "Identify the grammatical error in the report.",
                    "max_score": 12,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Find the error in the sentence: 'There is five computers.'",
                            "options": [
                                {"text": "is (should be 'are')", "is_correct": True},
                                {"text": "five (should be '5')", "is_correct": False},
                                {"text": "computers (should be 'computer')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'There are a robot.'",
                            "options": [
                                {"text": "are (should be 'is')", "is_correct": True},
                                {"text": "a (should be 'an')", "is_correct": False},
                                {"text": "robot (should be 'robots')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'There is books.'",
                            "options": [
                                {"text": "is (should be 'are')", "is_correct": True},
                                {"text": "books (should be 'book')", "is_correct": False},
                                {"text": "There (should be 'Their')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'There is five photos.'",
                            "options": [
                                {"text": "is (should be 'are')", "is_correct": True},
                                {"text": "five (should be '5')", "is_correct": False},
                                {"text": "photos (should be 'photo')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'There are a friendly alien.'",
                            "options": [
                                {"text": "are (should be 'is')", "is_correct": True},
                                {"text": "a (should be 'an')", "is_correct": False},
                                {"text": "friendly (should be 'friend')", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Writing: Discovery Report",
                    "desc": "Write what you can see in each area (Study Room & Garden) to help us remember our spaceship.",
                    "max_score": 20,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Write a report describing what is inside the study room and the spaceship garden. (Use there is / there are)",
                            "is_free_text": True
                        }
                    ]
                }
            ]
        },
        # ==========================================
        # DAY 3: Daily Routines on the Spaceship
        # ==========================================
        {
            "day_num": 3,
            "title": "Day 3 - Dimension 3: Daily Routines",
            "desc": "Present Simple (Subject + base verb, He/She/It + verb + s/es).",
            "mission_title": "A Normal Day on the Spaceship",
            "story": "A Normal Day on the Spaceship: The General wakes up at 7:00, eats cereal and drinks milk. He meets the Trainer who eats fruits and trains. A recruit cleans the control room, and another studies English and sleeps early.",
            "activities": [
                {
                    "title": "Reading: Comic - Daily Routines on the Spaceship",
                    "desc": "Read about the daily routines of the spaceship crew and answer the questions.",
                    "max_score": 10,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "What does the General do before checking the crew?",
                            "options": [
                                {"text": "Wakes up at 7:00, eats cereal and drinks milk", "is_correct": True},
                                {"text": "Cleans the control room", "is_correct": False},
                                {"text": "Trains in the gym", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does the Trainer do every morning?",
                            "options": [
                                {"text": "Eats fruits and trains", "is_correct": True},
                                {"text": "Wakes up at 9:00", "is_correct": False},
                                {"text": "Writes reports", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does the recruit study?",
                            "options": [
                                {"text": "English", "is_correct": True},
                                {"text": "Science", "is_correct": False},
                                {"text": "Space navigation", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does the recruit do after lunch?",
                            "options": [
                                {"text": "Cleans the control room", "is_correct": True},
                                {"text": "Sleeps early", "is_correct": False},
                                {"text": "Plays video games", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does the General do every day?",
                            "options": [
                                {"text": "Writes and reads daily reports", "is_correct": True},
                                {"text": "Cleans the engine", "is_correct": False},
                                {"text": "Explores planets", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Grammar: Mission 1 - Sentence Launch",
                    "desc": "Arrange the scrambled words to form correct sentences.",
                    "max_score": 10,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Arrange the words to form a correct sentence: trains / every morning / the Trainer",
                            "options": [{"text": "The Trainer trains every morning.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: studies / English / the recruit",
                            "options": [{"text": "The recruit studies English.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: control room / cleans / the recruit / the",
                            "options": [{"text": "The recruit cleans the control room.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: writes / reports / the General",
                            "options": [{"text": "The General writes reports.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: sleeps / early / he",
                            "options": [{"text": "He sleeps early.", "is_correct": True}]
                        }
                    ]
                },
                {
                    "title": "Mission 2: Word Recovery Zone",
                    "desc": "Select the correct form of the verb to fill in the blank.",
                    "max_score": 8,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "The Trainer ___ every morning.",
                            "options": [
                                {"text": "trains", "is_correct": True},
                                {"text": "train", "is_correct": False},
                                {"text": "training", "is_correct": False}
                            ]
                        },
                        {
                            "text": "The recruit ___ English every day.",
                            "options": [
                                {"text": "studies", "is_correct": True},
                                {"text": "study", "is_correct": False},
                                {"text": "studying", "is_correct": False}
                            ]
                        },
                        {
                            "text": "The recruit ___ the control room.",
                            "options": [
                                {"text": "cleans", "is_correct": True},
                                {"text": "clean", "is_correct": False},
                                {"text": "cleaning", "is_correct": False}
                            ]
                        },
                        {
                            "text": "The General ___ reports every day.",
                            "options": [
                                {"text": "writes", "is_correct": True},
                                {"text": "write", "is_correct": False},
                                {"text": "writing", "is_correct": False}
                            ]
                        },
                        {
                            "text": "The General ___ cereal in the morning.",
                            "options": [
                                {"text": "eats", "is_correct": True},
                                {"text": "eat", "is_correct": False},
                                {"text": "eating", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Mission 3: Ship Repair - Error Detection",
                    "desc": "Identify the grammatical error in the routines log.",
                    "max_score": 12,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Find the error in the sentence: 'The Trainer train every morning.'",
                            "options": [
                                {"text": "train (should be 'trains')", "is_correct": True},
                                {"text": "Trainer (should be 'Trainers')", "is_correct": False},
                                {"text": "every (should be 'all')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'The recruit study English every day.'",
                            "options": [
                                {"text": "study (should be 'studies')", "is_correct": True},
                                {"text": "recruit (should be 'recruits')", "is_correct": False},
                                {"text": "English (should be 'english')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'The General write reports.'",
                            "options": [
                                {"text": "write (should be 'writes')", "is_correct": True},
                                {"text": "General (should be 'Generals')", "is_correct": False},
                                {"text": "reports (should be 'report')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'He eat cereal in the morning.'",
                            "options": [
                                {"text": "eat (should be 'eats')", "is_correct": True},
                                {"text": "cereal (should be 'cereals')", "is_correct": False},
                                {"text": "morning (should be 'mornings')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'She clean the control room.'",
                            "options": [
                                {"text": "clean (should be 'cleans')", "is_correct": True},
                                {"text": "control (should be 'controls')", "is_correct": False},
                                {"text": "room (should be 'rooms')", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Writing: Daily Routine schedule",
                    "desc": "Share your daily schedule with your friend recruit so you can find a time to meet. Use the template.",
                    "max_score": 20,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Write a letter to your friend describing your routines. (e.g. In the morning I wake up at... In the afternoon I study... In the evening I sleep...)",
                            "is_free_text": True
                        }
                    ]
                }
            ]
        },
        # ==========================================
        # DAY 4: What Are You Doing Today?
        # ==========================================
        {
            "day_num": 4,
            "title": "Day 4 - Dimension 4: Present Continuous",
            "desc": "Present Continuous (Subject + am/is/are + verb + ing) for actions right now.",
            "mission_title": "Crew Inspection",
            "story": "Crew Inspection: The General is sick, so you supervise the crew. Recruit 1 is studying English, Recruit 2 is cleaning the control room, another is reading a space guide, another is writing a report, and one is eating lunch.",
            "activities": [
                {
                    "title": "Reading: Comic - What Are You Doing Today?",
                    "desc": "Read about what the crew is doing right now and answer the questions.",
                    "max_score": 10,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Why are you supervising the recruits?",
                            "options": [
                                {"text": "The General is sick", "is_correct": True},
                                {"text": "The General is exploring a planet", "is_correct": False},
                                {"text": "You are the Trainer", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What is Recruit 1 doing?",
                            "options": [
                                {"text": "Studying English", "is_correct": True},
                                {"text": "Cleaning the room", "is_correct": False},
                                {"text": "Eating lunch", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Where is the recruit who is writing?",
                            "options": [
                                {"text": "In the communication center", "is_correct": True},
                                {"text": "In the cafeteria", "is_correct": False},
                                {"text": "In the study room", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What is the recruit in the cafeteria doing?",
                            "options": [
                                {"text": "Eating lunch", "is_correct": True},
                                {"text": "Cleaning the floor", "is_correct": False},
                                {"text": "Reading a book", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What is the last recruit reading?",
                            "options": [
                                {"text": "A space guide", "is_correct": True},
                                {"text": "A comic book", "is_correct": False},
                                {"text": "An English exam", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Grammar: Mission 1 - Sentence Launch",
                    "desc": "Arrange the scrambled words to form correct sentences.",
                    "max_score": 10,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Arrange the words to form a correct sentence: studying / I / am / English",
                            "options": [{"text": "I am studying English.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: is / She / writing / report / a",
                            "options": [{"text": "She is writing a report.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: lunch / eating / are / They",
                            "options": [{"text": "They are eating lunch.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: project / working / He / a / on / is",
                            "options": [{"text": "He is working on a project.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: drawing / We / map / a / are",
                            "options": [{"text": "We are drawing a map.", "is_correct": True}]
                        }
                    ]
                },
                {
                    "title": "Mission 2: Word Recovery Zone",
                    "desc": "Select the correct combination to complete the sentence.",
                    "max_score": 8,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "I ___ studying English.",
                            "options": [
                                {"text": "am", "is_correct": True},
                                {"text": "is", "is_correct": False},
                                {"text": "are", "is_correct": False}
                            ]
                        },
                        {
                            "text": "She is ___ a report.",
                            "options": [
                                {"text": "writing", "is_correct": True},
                                {"text": "write", "is_correct": False},
                                {"text": "writes", "is_correct": False}
                            ]
                        },
                        {
                            "text": "They ___ eating lunch.",
                            "options": [
                                {"text": "are", "is_correct": True},
                                {"text": "am", "is_correct": False},
                                {"text": "is", "is_correct": False}
                            ]
                        },
                        {
                            "text": "He is working ___ a project.",
                            "options": [
                                {"text": "on", "is_correct": True},
                                {"text": "in", "is_correct": False},
                                {"text": "at", "is_correct": False}
                            ]
                        },
                        {
                            "text": "We are drawing ___ map.",
                            "options": [
                                {"text": "a", "is_correct": True},
                                {"text": "an", "is_correct": False},
                                {"text": "any", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Mission 3: Ship Repair - Error Detection",
                    "desc": "Identify the grammatical error in the present continuous logs.",
                    "max_score": 12,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Find the error in the sentence: 'I am study English.'",
                            "options": [
                                {"text": "study (should be 'studying')", "is_correct": True},
                                {"text": "am (should be 'is')", "is_correct": False},
                                {"text": "English (should be 'english')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'She is write a report.'",
                            "options": [
                                {"text": "write (should be 'writing')", "is_correct": True},
                                {"text": "is (should be 'are')", "is_correct": False},
                                {"text": "a (should be 'an')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'They are eat lunch.'",
                            "options": [
                                {"text": "eat (should be 'eating')", "is_correct": True},
                                {"text": "are (should be 'is')", "is_correct": False},
                                {"text": "lunch (should be 'lunches')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'He is work on a project.'",
                            "options": [
                                {"text": "work (should be 'working')", "is_correct": True},
                                {"text": "on (should be 'at')", "is_correct": False},
                                {"text": "a (should be 'an')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'We are draw a map.'",
                            "options": [
                                {"text": "draw (should be 'drawing')", "is_correct": True},
                                {"text": "are (should be 'is')", "is_correct": False},
                                {"text": "map (should be 'maps')", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Writing: Report to the General",
                    "desc": "Write a short progress report for the General about what the crew is doing right now.",
                    "max_score": 20,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Write a progress report for the General using the Present Continuous (e.g. Recruit 1 is studying..., They are eating...)",
                            "is_free_text": True
                        }
                    ]
                }
            ]
        },
        # ==========================================
        # DAY 5: Habits and Frequency
        # ==========================================
        {
            "day_num": 5,
            "title": "Day 5 - Dimension 5: Frequency",
            "desc": "How often, What time, Adverbs of frequency (always, sometimes, never).",
            "mission_title": "Lunch Time Chat",
            "story": "Lunch Time Chat: The crew eats lunch in the garden. Your friend says: I always wake up at 6:00 a.m. and study English at 4:00 p.m. I sometimes train at 5:00 p.m. I always help new recruits, and sometimes explore Basescrib. I never draw during missions.",
            "activities": [
                {
                    "title": "Reading: Comic - Lunch Time Chat",
                    "desc": "Read about the crew's habits and adverbs of frequency, and answer the questions.",
                    "max_score": 10,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Where is the crew eating lunch?",
                            "options": [
                                {"text": "Spaceship garden", "is_correct": True},
                                {"text": "Control room", "is_correct": False},
                                {"text": "Cafeteria", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What time does the friend recruit always wake up?",
                            "options": [
                                {"text": "6:00 a.m.", "is_correct": True},
                                {"text": "7:00 a.m.", "is_correct": False},
                                {"text": "3:00 p.m.", "is_correct": False}
                            ]
                        },
                        {
                            "text": "What does he sometimes do at 5:00 p.m.?",
                            "options": [
                                {"text": "Train", "is_correct": True},
                                {"text": "Study English", "is_correct": False},
                                {"text": "Sleep", "is_correct": False}
                            ]
                        },
                        {
                            "text": "How often does he help new recruits?",
                            "options": [
                                {"text": "Always", "is_correct": True},
                                {"text": "Sometimes", "is_correct": False},
                                {"text": "Never", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Does he sleep at 3:00 p.m.?",
                            "options": [
                                {"text": "No, he never sleeps at 3:00 p.m.", "is_correct": True},
                                {"text": "Yes, he always sleeps at 3:00 p.m.", "is_correct": False},
                                {"text": "Yes, he sometimes sleeps at 3:00 p.m.", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Grammar: Mission 1 - Sentence Launch",
                    "desc": "Arrange the scrambled words to form correct sentences.",
                    "max_score": 10,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Arrange the words to form a correct sentence: always / wake up / I / at 6:00 a.m.",
                            "options": [{"text": "I always wake up at 6:00 a.m.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: sometimes / train / I / at 5:00 p.m.",
                            "options": [{"text": "I sometimes train at 5:00 p.m.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: new recruits / always / help / I",
                            "options": [{"text": "I always help new recruits.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: Basescrib / sometimes / explore / I",
                            "options": [{"text": "I sometimes explore Basescrib.", "is_correct": True}]
                        },
                        {
                            "text": "Arrange the words to form a correct sentence: never / sleep / I / at 3:00 p.m.",
                            "options": [{"text": "I never sleep at 3:00 p.m.", "is_correct": True}]
                        }
                    ]
                },
                {
                    "title": "Mission 2: Word Recovery Zone",
                    "desc": "Select the correct combination to complete the habit log.",
                    "max_score": 8,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "I ___ study English at 4:00 p.m.",
                            "options": [
                                {"text": "always", "is_correct": True},
                                {"text": "draw", "is_correct": False},
                                {"text": "are", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I sometimes ___ at 5:00 p.m.",
                            "options": [
                                {"text": "train", "is_correct": True},
                                {"text": "trains", "is_correct": False},
                                {"text": "training", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I always help new ___.",
                            "options": [
                                {"text": "recruits", "is_correct": True},
                                {"text": "recruit", "is_correct": False},
                                {"text": "recruiting", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I sometimes ___ my friends.",
                            "options": [
                                {"text": "meet", "is_correct": True},
                                {"text": "meets", "is_correct": False},
                                {"text": "meeting", "is_correct": False}
                            ]
                        },
                        {
                            "text": "I never ___ at 3:00 p.m.",
                            "options": [
                                {"text": "sleep", "is_correct": True},
                                {"text": "sleeps", "is_correct": False},
                                {"text": "sleeping", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Mission 3: Ship Repair - Error Detection",
                    "desc": "Identify the grammatical error in the frequency logs.",
                    "max_score": 12,
                    "is_open": False,
                    "questions": [
                        {
                            "text": "Find the error in the sentence: 'I always wake up at 6:00 p.m.'",
                            "options": [
                                {"text": "p.m. (should be 'a.m.')", "is_correct": True},
                                {"text": "always (should be 'never')", "is_correct": False},
                                {"text": "wake (should be 'wakes')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I never train at 5:00 p.m.'",
                            "options": [
                                {"text": "never (should be 'sometimes')", "is_correct": True},
                                {"text": "train (should be 'trains')", "is_correct": False},
                                {"text": "p.m. (should be 'a.m.')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I sometimes helps new recruits.'",
                            "options": [
                                {"text": "helps (should be 'help')", "is_correct": True},
                                {"text": "sometimes (should be 'always')", "is_correct": False},
                                {"text": "recruits (should be 'recruit')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I always explores Basescrib.'",
                            "options": [
                                {"text": "explores (should be 'explore')", "is_correct": True},
                                {"text": "always (should be 'sometimes')", "is_correct": False},
                                {"text": "Basescrib (should be 'Basescribs')", "is_correct": False}
                            ]
                        },
                        {
                            "text": "Find the error in the sentence: 'I always sleep at 3:00 p.m.'",
                            "options": [
                                {"text": "always (should be 'never')", "is_correct": True},
                                {"text": "sleep (should be 'sleeps')", "is_correct": False},
                                {"text": "p.m. (should be 'a.m.')", "is_correct": False}
                            ]
                        }
                    ]
                },
                {
                    "title": "Writing: Crew Habit Survey",
                    "desc": "Complete the survey describing your own frequency of habits.",
                    "max_score": 20,
                    "is_open": True,
                    "questions": [
                        {
                            "text": "Answer how often you perform these actions: 1. Wake up early? 2. Study English? 3. Train? 4. Help new recruits? 5. Meet friends?",
                            "is_free_text": True
                        }
                    ]
                }
            ]
        }
    ]

    # Populate loop
    for day in curriculum:
        # 1. Create Level
        level_obj = Level.objects.create(
            code=f"L{day['day_num']}",
            title=day['title'],
            description=day['desc'],
            order=day['day_num']
        )
        print(f"Created Level: {level_obj.title}")

        # 2. Create Mission
        mission_obj = Mission.objects.create(
            title=day['mission_title'],
            description=day['story'],
            level=level_obj,
            order=1,
            unlock_code=""
        )
        print(f"  Created Mission: {mission_obj.title}")

        # 3. Create Activities
        for idx, act in enumerate(day['activities']):
            activity_obj = Activity.objects.create(
                mission=mission_obj,
                title=act['title'],
                description=act['desc'],
                is_open=act['is_open'],
                max_score=act['max_score']
            )
            print(f"    Created Activity: {activity_obj.title} (ID: {activity_obj.id})")

            # 4. Create Questions
            for q in act['questions']:
                is_free_text = q.get('is_free_text', False)
                question_obj = Question.objects.create(
                    activity=activity_obj,
                    text=q['text'],
                    is_free_text=is_free_text
                )

                # 5. Create AnswerOptions if multiple choice
                if not is_free_text:
                    for opt in q.get('options', []):
                        AnswerOption.objects.create(
                            question=question_obj,
                            text=opt['text'],
                            is_correct=opt['is_correct']
                        )

    print("Successfully structured and populated database with all 5 Days of curriculum!")

if __name__ == '__main__':
    populate()
