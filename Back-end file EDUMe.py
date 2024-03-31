questions_list = ["What learning styles work best for you?",
                "Which types of content do you find more accessible or engaging?",
                "Do you prefer interactive learning materials (e.g., quizzes, simulations, interactive exercises) or more traditional formats (e.g., textbooks, lectures)?",
                "Amongst the following learning strategies or techniques, are there any that you find particularly effective for retaining information?", 
                "When learning new concepts, do you prefer step-by-step instructions, visual diagrams, or verbal explanations?", 
                "How do you prefer to organize and review study materials?"]

answers_list = [["a) visual", "b) auditory", "c)kinesthetic"],
               ["a)text", "b)audio", "c)video"],
               ["a)both", "b)traditional methods","c)interactive learning materials",],
               ["a)active recall", "b)practice testing", "c)multi-sensory learning"],
               ["a) visual diagrams","b)verbal explanations", "c)step-by-step instructions"],
               ["a) written notes", "b)verbal repetition", "c)digital flashcards"],]
i = 0 
score_counter = 0
for questions, answers in zip(questions_list, answers_list):
    while i<5:
        print(questions_list[i] + '\n' + ' '.join(answers_list[i])+'\n')
        get_answer = input()
        if (get_answer != "a" and get_answer != "b" and get_answer != "c"):
            {
            print("Invalid, enter 'a, b or c'")
        }
        else: i += 1
        if (get_answer == "a"):
            score_counter += 1
        elif (get_answer == "b"):
            score_counter += 2
        elif (get_answer == "c"):
            score_counter += 3

if (5<= score_counter< 9):
    disability = "auditory processing disorder (APD), Non verbal learning disabilities(NVLD"

if (9<= score_counter< 13):
    disability = "dysgraphia or visual motor deficit"

if (13<= score_counter< 18):
    disability = "ADHD or dyslexia"

print("\n")
name = input("What is your name? ")
age = input("How old are you? ")

print(f"you may be affected by qualities similar to those who are suffering from {disability}.")

from openai import OpenAI

client = OpenAI(api_key="API_KEY")

messages = []
system_msg = f"You are a special needs tutor teaching {name} who is {age} years old. They have trouble learning the conventional way and have {disability}. They need you, a special tutor, to help them with their learning."
messages.append({"role": "system", "content": system_msg})

message =  f"Provide a percentage split of how much of their learning should be text, and how much should be video based on their {disability}.Provide in the format (percentage of video) and (percentage of text) on the next line. Do not provide any other information Only display the two percentages without the percent sign on two separate lines (just numbers and no text)."
messages.append({"role": "user", "content": message})
response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=messages)
content = response.choices[0].message.content

video = 0
text = 0

lines = content.split('\n')

video = (int(lines[0]))/10
text = (int(lines[1]))/10

if text == 0:
    text = 1

from googleapiclient.discovery import build

content = input("What would you like to learn today?")
quiz_results = ""

quiz = False
print("We believe that the following breakdown of educational content would help you learn best: \n\n")
while quiz == False:

    api_key = "API_KEY"
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part="snippet",
        q=content,  
        maxResults= video,
        type="video"
    )

    response = request.execute()


    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        thumbnail_url = item['snippet']['thumbnails']['high']['url']
        
        print(f"Title: {title}")
        print(f"Video URL: {video_url}") 
        print("\n")

    sentences = text*3

    message =  f"Provide a description to the person that is easy to understand and takes into account their {disability}. Make sure to explain the concept in a way that they can understand. Make the description of {content} only {sentences} number of sentences. {quiz_results}"
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    content = response.choices[0].message.content
    print (content)

    message = f"""
    Generate a quiz based on {content}. Create two true or false questions related to the content. Present the quiz in the following format:

    Question 1: [content of question 1]
    [answer 1 (T or F)]
    Question 2: [content of question 2]
    [answer 2 (T or F)]

    Ensure that:
    - The first and third lines display the questions only.
    - The second and fourth lines display the answers as either 'T' or 'F', nothing else.
    """
    messages.append({"role": "user", "content": message})
    response = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=messages)
    content = response.choices[0].message.content

    lines = content.split('\n')

    q1 = lines[0]
    q2 = lines [2]
    ans1 = lines[1]
    ans2 = lines[3]

    user_ans1 = input(q1)
    user_ans2 = input(q2)

    if user_ans1!= ans1 or user_ans2!=ans2:
        quiz = False
        print("\nLooks like you did not answer both of the questions correctly. Let's try a new approach to learning this topic.\n")
        quiz_results = f"{name} did not learn effectively and got some quiz questions on this {content} wrong. In {sentences} sentences, explain the {content} in a better way for {name} with {disability} to understand. For etxra context, they had difficulty answer {q1} and {q2}"

    else:
        quiz = True

print("Thanks for using EDUMe. Take care! ")
