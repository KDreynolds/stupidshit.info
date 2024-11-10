from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import requests
from datetime import datetime

app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'

# Function to format date
def format_date(date_str):
    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime('%B %d, %Y')

@app.template_filter('date_format')
def date_format(value):
    try:
        date_obj = datetime.fromisoformat(value)
        return date_obj.strftime('%B %d, %Y')
    except ValueError:
        return value

app.jinja_env.filters['date_format'] = date_format

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for landing page - loads posts from JSON
@app.route('/landing')
def landing():
    posts = [
 	 {
       	    "title": "The Power of Collaboration in Software Development",
            "content": "As software engineers, we often find ourselves immersed in our own projects, focused on solving complex problems and crafting elegant code. However, we shouldn't underestimate the tremendous value of collaboration in our field.\n\nCollaboration allows us to learn from one another, share insights, and collectively tackle challenges that might seem insurmountable alone. When we work together, we expose ourselves to new perspectives, techniques, and problem-solving approaches. We can learn from the successes and failures of our peers, and in turn, share our own experiences to help others grow.\n\nMoreover, collaboration fosters creativity and innovation. By bouncing ideas off each other, we can spark new solutions and push the boundaries of what's possible. Diverse viewpoints and skill sets come together to create something greater than the sum of its parts.\n\nCollaboration also extends beyond our immediate teams. Engaging with the wider developer community, whether through open source projects, online forums, or local meetups, allows us to tap into a vast pool of knowledge and contribute to the collective advancement of our field.\n\nSo, next time you find yourself stuck or in need of inspiration, remember the power of collaboration. Reach out to your colleagues, participate in code reviews, contribute to shared projects, and engage with the community. Together, we can build amazing things and propel the world of software development forward.",
            "date": "2024-04-10"
   	 },
   	 {
        "title": "Don't Burn Yourself Out",
        "content": "Taking breaks is essential for software engineers to maintain productivity and avoid burnout. While it may seem counterintuitive, strategic breaks can actually boost your efficiency and creativity. When you step away from your work, you allow your brain to process information, generate new ideas, and prevent mental fatigue. To make the most of your breaks, try techniques like the Pomodoro method (25-minute work intervals with 5-minute breaks), the 52/17 rule (52 minutes of work followed by a 17-minute break), or microbreaks (1-2 minute breaks every 20-30 minutes). During longer breaks, engage in non-screen activities such as walking or reading. By incorporating strategic breaks into your workday, you can improve your overall performance and well-being as a software engineer.",
        "date": "2024-04-08"
   	 },
   	 {
        "title": "March Madness Competition Complete",
        "content": "Phew, that competition ended up taking up a whole lot more time than I thought it was going to. I did not do nearly as well as I was hoping to do but also this was my first Kaggle competition and I learned a lot about the space and have a lot of ideas moving forward on how to improve. I have been messing around now with possibly starting another competition, as I have been having a sort of Coders block recently where I just don't know what to work on. This is a pretty strange position for me to be in to be honest. Maybe I need to rest my brain a little bit haha.",
        "date": "2024-04-03"
   	 },
       	 {
        "title": "March Madness Kaggle Competition 2024",
        "content": "Alright so to mix it up a little bit this year, I have entered the Kaggle 2024 March Madness competition. The first step in building our model is to gather historical data. We collected data on regular season games, tournament results, and various team statistics. This data includes features like win-loss records, offensive and defensive efficiency ratings, strength of schedule, and more. Next, we performed feature engineering to create new variables that capture important information. For example, we calculated the difference in winning percentages between teams, their head-to-head records, and their performance in the last 5 and 10 games leading up to the tournament. With our data prepared, we split it into training and validation sets. We then trained a Histogram-based Gradient Boosting Classification Tree model using the scikit-learn library in Python. This model was chosen because it can handle missing values and provides good interpretability. To find the best hyperparameters for our model, we performed a grid search with cross-validation. This process helped us identify the optimal values for parameters like maximum depth, learning rate, and number of estimators. After training our model, we evaluated its performance on the validation set. We achieved an accuracy of 68%, which is a significant improvement over random guessing (50% accuracy) and the performance of many human experts. There is still a lot of work to do before we are ready to submit our model but I am feeling pretty good about this.",
        "date": "2024-03-14"
   	 },
   	 {
        "title": "Reading Other Peoples Code is Super Important",
        "content": "One oft overlooked skill in the repertoire of the software developer, is reading other peoples code. Much like reading new authors and/or books, you never really know what sort of things will turn out to be inspiring to you. Today I was just really impressed with the comments in a particular codebase and it made me completely rethink the way i comment in my code. It's hard to really put a cap on the sort of things you can improve in your own code this way, they are endless, ranging from minuscule to monumental. Maybe this is just so obvious to me because I spend so much time in the Open Source world but think of it like taking a mental walk every once in awhile. Read a codebase you have nothing to do with just for fun.",
        "date": "2024-03-05"
   	 },
   	 {
        "title": "Thoughts on Clean Code and Other Dogmatic Bullshit",
        "content": "From the title there you can probably guess how I feel about 'Clean Code' and other similar, dogmatic approaches to writing code/software. I think largely these type of approaches quickly lose sight of the original goals you had in writing your code and quickly turn into a snake eating it's own tail. For some reason I am always reminded of one of my favorite Kurt Vonnegut ideas when I think about the problems with Clean Code and similar approaches, In A Man Without a Country, Vonnegut discusses how Bepop Jazz influenced his style of writing in that it pushed him to break every rule he could think of. It is a lot easier to parse what rules are actually important and what rules can be tossed aside when you just go out and break them all. I think my point is, Do not take these dogmatic, over-arching musings as gospel, go out and break some shit so you have the experience under your belt.",
        "date": "2024-03-03"
   	 },
   	 {
        "title": "I'm Dumb and That Is Good Actually",
        "content": "Software engineers are often hailed as some of the brightest minds around, well, most of them, not including myself, of course. I'm here today, not to boast about complex algorithms or sophisticated design patterns, but to champion the cause of simplicity in our craft. In the dazzling world of tech, where complexity is often worn as a badge of honor, I've found solace in keeping things straightforward. It's a plea to my fellow developers: before you go down the rabbit hole of over-engineering, ask yourself, \"Is there a simpler way?\" Complexity isn't just a barrier to entry for those of us trying to understand or modify code; it's also a breeding ground for bugs and maintenance nightmares. I'm advocating for simplicity not because I shun challenge, but because I believe in efficiency. Writing code that is as simple as possible means anyone can understand it, maintain it, and build upon it. Imagine you're crafting a tool. A rock might serve your purpose just fine until you realize you need a hammer. The lesson here? Don't start with a Swiss Army knife when a simple screwdriver will do. The elegance in engineering lies not in the complexity of solutions, but in finding simple solutions to complex problems. Remember, the goal is to solve problems, not to showcase our intellectual prowess.",
        "date": "2024-02-27"
   	 },
   	 {
        "title": "Self Taught vs. University",
        "content": "Navigating the waters of a software engineering career can be daunting, especially when you're steering the ship with a self-taught compass. As someone who's traveled this route, I've felt both the liberation of charting my own course and the weight of gaps in my knowledge. Earning a degree in Computer Science undoubtedly opens doors and lays a solid foundation of principles and practices. It's a structured path that offers exposure to a breadth of subjects, from algorithms and data structures to systems design and beyond. The university environment also fosters networking, mentorship, and collaboration, invaluable assets in the tech industry. However, the self-taught journey, while rugged, is marked by a relentless pursuit of knowledge, driven by curiosity and practical application. It's a testament to the accessibility of resources and the democratization of learning. The internet is a treasure trove of tutorials, forums, and open-source projects, offering endless opportunities to learn and contribute. But here's the catch: being self-taught requires discipline, direction, and a willingness to embrace failure as a teacher. It's a path of constant catch-up, trying to plug the holes in your knowledge while simultaneously pushing forward. If given the chance to rewind time, would I opt for a formal degree? Yes, without hesitation. But do I regret the path I've taken? Absolutely not. It's shaped me into a resourceful, resilient engineer, and it's a viable route for those who, for whatever reason, can't take the traditional path. Both paths lead to the same destination: becoming a competent software engineer. The choice between self-taught and university isn't about which is better overall, but which is better for you, your learning style, and your circumstances.",
        "date": "2024-02-26"
   	 },
   	 {
        "title": "Chat GPT Should be your new Google",
        "content": "There's a new player in town, and it's changing the way we, as software engineers, solve problems and learn: ChatGPT. While Google has been our trusty sidekick for years, enabling us to sift through countless forums, documentation pages, and Stack Overflow answers, ChatGPT offers a more streamlined, efficient alternative. Instead of combing through multiple websites to find the most relevant solution, you can now have a conversation with an AI that's been trained on a vast amount of programming knowledge. ChatGPT can understand complex queries and provide explanations, code examples, and even debug suggestions in seconds. It's like having a mentor available 24/7, ready to help you untangle the most convoluted code or grasp new concepts without the need to decipher which link on the search results page will lead you to the information you need. Plus, it's continually learning from its interactions, meaning it gets better and more insightful with every question asked. But here's the kicker: you don't have to abandon Google entirely. ChatGPT isn't just a replacement; it's a supplement. It excels in direct interaction and can guide you to the precise knowledge you seek, but sometimes, a deep dive into documentation or a forum discussion via a Google search can complement the insights provided by ChatGPT. The key is knowing when to leverage this AI tool for efficiency and when the broader context of a Google search might offer additional value. In conclusion, ChatGPT represents a paradigm shift in how we approach problem-solving and learning in software development. It offers a direct line to the information we need, saving us time and helping us stay focused on the task at hand. So, next time you're stuck or curious, consider asking ChatGPT first. It might just become your new favorite tool in your developer toolkit.",
        "date": "2024-02-25"
   	 },
   	 {
        "title": "Embrace the Side Projects: They're More Than Just Hobbies",
        "content": "Side projects are often seen as the playground for developers, a space where we can experiment, learn, and fail without the pressure of deadlines or clients breathing down our necks. But they're so much more than that. Through my own journey of building random apps, tools, and websites on the side, I've learned valuable skills that my day job never touched on. I was able to teach myself to code in the first place by just building the things I wanted to build and playing around with new technology. It's this curiuosity that I have found to be tantamount to improving as a developer. I think a lot of newer engineers get hung up on what they should build and with what tech, etc. In the end it doesn't really matter at all. Just that you are building.",
        "date": "2024-02-24"
   	 },
    ]

    for post in posts:
        post['date'] = format_date(post['date'])
    return render_template('landing.html', posts=posts)

# Route for sending form data to Google Sheets via NoCodeAPI
@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        form_data = {
            "Name": name,
            "Email": email,
            "Message": message
        }
        data = [[form_data['Name'], form_data['Email'], form_data['Message']]]

        # Send data to the Google Sheets API via Nocodeapi
        url = "https://v1.nocodeapi.com/kdreynolds/google_sheets/QEpNwsnHlEBZIPDQ?tabId=Sheet1"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        if response.ok:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": "Failed to send data"}), 500

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Server error"}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=7000, debug=True)
