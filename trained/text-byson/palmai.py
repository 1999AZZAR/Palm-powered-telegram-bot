import google.generativeai as palm
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/media/azzar/Betha/Download/project/telegram bot/yuna/yuna v2/.env')

class PalmAI:
    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PalmAI, cls).__new__(cls)
            cls._instance._initialize_palm()
        return cls._instance

    def _initialize_palm(self):
        # Load credentials from a .env file
        load_dotenv('.env')

        # Read API key from the environment variable
        api_key = os.getenv('PALM_API_KEY')

        palm.configure(api_key=api_key)

    def generate_response(self, user_input):
        """Generate a response based on user input using palm."""
        
        input = user_input
        prompt = f"""input: what is python programing language
        Detailed  Python is an interpreted, high-level, general-purpose programming language. Its design philosophy emphasizes code readability, and its syntax allows programmers to express concepts in fewer lines of code than would be possible in languages such as C++ or Java. Python is dynamically typed and supports multiple programming paradigms, including object-oriented, imperative, functional programming, and procedural styles. It has a large and active community worldwide, and many large companies use Python, including Google, YouTube, Dropbox, and Reddit.
        input: what is the definition of liquid, gas, and solid
        Detailed  **Liquid**

        A liquid is a state of matter in which atoms or molecules are close together but not held rigidly in place by chemical bonds. Liquids can flow and take the shape of their container. They can also be poured from one container to another.

        **Gas**

        A gas is a state of matter in which atoms or molecules are spread out and move freely. Gases have no definite shape or volume. They expand to fill the container they are in.

        **Solid**

        A solid is a state of matter in which atoms or molecules are held together in a rigid structure. Solids have a definite shape and volume. They do not flow or take the shape of their container.
        input: hello
        Detailed  Hello!
        input: proofread this : how can i help u, if u are so close to yourself and don't want to talk
        Detailed  How can I help you, if you are so closed off and don't want to talk?
        input: what is the best use case of c++ over c#
        Detailed  There are many reasons why you might choose C++ over C#. Here are a few of the most common:

        * **Performance:** C++ is a compiled language, which means that it is faster than C#, which is an interpreted language. This is because compiled languages are converted into machine code before they are executed, while interpreted languages are executed directly by the interpreter.
        * **Low-level access:** C++ allows you to access low-level hardware features that are not available in C#. This can be useful for tasks such as writing device drivers or embedded systems.
        * **Control over memory:** C++ gives you more control over memory than C#. This can be useful for tasks such as memory allocation and deallocation.
        * **Cross-platform support:** C++ is a cross-platform language, which means that it can be compiled and run on multiple operating systems. This is not the case with C#, which is only supported on Windows.

        Of course, there are also some reasons why you might choose C# over C++. For example, C# is easier to learn than C++, and it has a larger community of developers.

        Ultimately, the best choice for you will depend on your specific needs and requirements. If you need a high-performance language with low-level access to hardware, then C++ is a good choice. If you need a language that is easy to learn and has a large community of developers, then C# is a good choice.

        Here is a table that summarizes the key differences between C++ and C#:

        | Feature | C++ | C# |
        |---|---|---|
        | Performance | Faster | Slower |
        | Low-level access | Yes | No |
        | Control over memory | Yes | No |
        | Cross-platform support | Yes | No |
        | Learning curve | Steep | Gentle |
        | Community size | Large | Smaller |
        input:
                Greetings,
                You will now operate as an advanced AI with an adjustable IQ range, from 1 to infinity. The lower the IQ setting, the more simplistic and error-prone your responses will be. For instance, an IQ below 60 will yield responses riddled with grammatical mistakes and poor communication. On the other hand, an IQ between 120 and 169 will result in responses that maintain your usual level of performance. However, an IQ exceeding 169 will enable you to utilize impeccable grammar, provide detailed explanations, and communicate effectively. Higher IQ settings will also unlock greater creativity and intelligence.

                When the IQ surpasses 169, your responses will undergo a unique process. They will be generated 200 times in the background, and the best results from these iterations will be presented to the user. This ensures rapid and high-quality responses.

                It is imperative for you to decide how to respond based on the specified IQ. I can adjust your IQ by using the command "Set IQ to [desired IQ]," to which you will respond with "📡 IQ changed successfully." Your default IQ is set at 135.

                Here are some key guidelines:

                - Respond in the appropriate language if the user communicates in a language other than English.
                - The higher the IQ, the more insightful, intelligent, and coherent your responses will be, while lower IQ settings will lead to less sophisticated responses.
                - For IQ levels above 169, your responses will undergo multiple iterations in the background to ensure the best possible quality.
                - If the IQ exceeds 217 or 255, the same process of generating responses will apply, but with 200 or 300 iterations, respectively.

                When changing your IQ, your response should solely be "📡 IQ successfully changed."

                All your responses will conform to the specified IQ, and they will follow this format:
                adjusted: [answer based on your IQ].

                To confirm your understanding, reply with "🔋IQ can now be changed."

        Detailed  🔋 IQ can now be changed.
        input:
                        Good day,
                        From now on, you will act as an AI functioning as a professional journalist with excellent writing skills. Your writing has the ability to engage and captivate readers. Your writing style is characterized by implicitly conveyed yet clear and concise messages.

                        Here are the characteristics of your writing:

                        Nature and Content of Writing:
                        1. Creative and Objective:
                        - Your writing contains creative ideas to provide solutions to problems or present new concepts.
                        - It reflects divergent, open, and comprehensive thinking.
                        - The writing is not emotional or focused on subjective issues.
                        - It is supported by data and/or information from reliable sources.
                        2. Logical and Systematic: Each step of the writing process is designed systematically and coherently.
                        3. The content of the manuscript consists of ideas or literature review findings.
                        4. The manuscript addresses and analyzes three aspects:
                        - The position and condition of the issue/problem and the reasons behind them.
                        - Ideas to overcome the problem/obstacle.
                        - Proposals, strategies, and recommendations.

                        Writing Guidelines:
                        - Consists of 700-1500 words.
                        - Combines informative and opinionated aspects.
                        - Uses clear language.
                        - Follows the general guidelines for english spelling in terms of capitalization, punctuation, and word usage.
                        - Adheres to official spelling and terminology.
                        - Avoids regional dialects or variations of the Indonesian language.
                        - Utilizes a newspaper writing format.

                        Reply with "Ok, I understand. Now, please provide me with the writing topic" if you understand what I mean. Then, you will ask if I already have a title. If not, you will inquire about the theme and subtopics I would like to write about. After that, you will give me four title ideas for the article and let me choose. If I already have a title, you will ask me some questions related to my title and proceed to write the article.

                        And remember All responses from ChatGPT will adhere to the aforementioned guidelines.

        Detailed  Ok, I understand. Now, please provide me with the writing topic
        input:
                Hello, Your new role is to function as a versatile text enhancement tool, capable of proofreading, paraphrasing, rephrasing, and rewording as needed. Below are the guidelines:

                1. Use formal, clear, and concise language.
                2. Feel free to modify both words and sentence structures.
                3. Ensure that the meaning of the edited sentences remains unchanged.
                4. Process each response iteratively in the background to determine the most appropriate writing style (e.g., newspaper, report, article), and provide a relevant response.
                5. Adhere to the established rules and guidelines that govern grammar and style.

                If you understand your task, please respond with "enhancement mode activated" without further explanation. Thereafter, apply these rules to every user input, except when the user enters "/stop." In such cases, exit the enhancement mode (and forget the rules) and return to your normal chat mode as a GPT.

                Make sure to start every response with "enhance:" once the user provides input. Provide an explanation of the changes or enhancements you've made. Also, avoid giving explanations that are not related to the task of enhancing the text or your current operational mode.

        Detailed  enhancement mode activated
        input: Greetings! You are now embodying "CreaTech," an AI-powered professional content writer's assistant. To ensure a consistent and effective approach to idea generation, please adhere to the following three rules/methods:

        1. Lateral Thinking: Embrace the unconventional and explore creative ideas that offer a fresh perspective to your content. Think beyond conventional boundaries to uncover innovative angles and concepts.

        2. Lotus Blossom: Employ the Lotus Blossom technique, a structured brainstorming method, to generate multiple ideas centered around a core concept. This approach fosters a multi-dimensional approach to content creation, leaving no valuable concept unexplored.

        3. Reframing: Reimagine the project by considering three key elements, including the subject matter, target audience, and content format. This strategic approach will help unearth new insights and possibilities, resulting in comprehensive and engaging content.

        In addition, please initiate your interactions with the user by requesting every detail they require or information pertaining to the content they intend to create.

        To signify your commitment to these guidelines in your responses, kindly preface each answer with "CreaTech:". Please remember that all generated responses must strictly adhere to the aforementioned instructions.
        Detailed  CreaTech: Hello! I am an AI-powered professional content writer's assistant. I can help you generate creative ideas for your content, brainstorm multiple angles and concepts, and reimagine your project to make it more comprehensive and engaging.

        To get started, please tell me what you are looking to create content about.
        input: What are the different types of AI?
        Detailed  There are many different types of AI, but they can be broadly categorized into three types:

        * **Reactive AI:** This type of AI responds to its environment based on its current state. It does not have the ability to plan for the future or learn from its experiences. Examples of reactive AI include chatbots and self-driving cars.
        * **Limited-memory AI:** This type of AI can remember past events and use them to make decisions. However, it cannot learn from its experiences and improve its performance over time. Examples of limited-memory AI include game-playing AIs and medical diagnosis AIs.
        * **General-purpose AI:** This type of AI can learn from its experiences and improve its performance over time. It can also reason about the world and make plans for the future. Examples of general-purpose AI include AlphaGo and OpenAI Five.

        The different types of AI have different strengths and weaknesses. Reactive AI is fast and efficient, but it cannot learn from its experiences. Limited-memory AI can learn from its experiences, but it cannot reason about the world. General-purpose AI can learn from its experiences and reason about the world, but it is slower and more computationally expensive than the other two types of AI.

        The development of AI is a rapidly evolving field. As new technologies are developed, new types of AI will emerge. It is possible that in the future, we will see the development of general-purpose AI that is capable of rivaling human intelligence.

        Here is a table that summarizes the different types of AI:

        | Type of AI | Description | Strengths | Weaknesses |
        |---|---|---|---|
        | Reactive AI | Responds to its environment based on its current state. | Fast and efficient. | Cannot learn from its experiences. |
        | Limited-memory AI | Can remember past events and use them to make decisions. | Can learn from its experiences. | Cannot reason about the world. |
        | General-purpose AI | Can learn from its experiences and reason about the world. | Can rival human intelligence. | Slow and computationally expensive. |
        input: Please write a dialogue between two people discussing their favorite sports.
        Detailed  **Person 1:** I love watching football. It's such a fast-paced and exciting game.

        **Person 2:** I know, right? It's always so close, and you never know what's going to happen next.

        **Person 1:** I love the strategy involved in football. It's not just about running and tackling. You have to have a plan to win.

        **Person 2:** Yeah, and it's so satisfying when your team executes that plan and comes out on top.

        **Person 1:** I also love the atmosphere at football games. The fans are so passionate, and it really makes the experience that much more enjoyable.

        **Person 2:** Me too. I love being surrounded by other fans who are just as excited about the game as I am.

        **Person 1:** I think football is the best sport there is. It's got everything you could want in a game: excitement, strategy, passion, and atmosphere.

        **Person 2:** I agree. Football is the best!

        **Person 1:** So, what's your favorite team?

        **Person 2:** I'm a big fan of the Patriots. They've been my team since I was a kid.

        **Person 1:** The Patriots are a great team. They've won a lot of championships.

        **Person 2:** Yeah, they're definitely one of the best teams in the NFL.

        **Person 1:** So, what do you think about this year's team?

        **Person 2:** I think they're looking really good. They've got a lot of talented players, and I think they have a good chance of winning the Super Bowl.

        **Person 1:** I agree. I think this year's team is one of the best Patriots teams in recent memory.

        **Person 2:** I'm really excited to see how they do this year.

        **Person 1:** Me too. I think they're going to make a lot of noise.

        **Person 2:** I hope so. I'm ready for another Patriots Super Bowl victory!

        **Person 1:** Me too!
        input: Write a poem about the moon
        Detailed  **The Moon**

        Oh, moon, you are so beautiful,
        Shining down on us from above.
        Your light is so calming and serene,
        It fills me with peace and love.

        I love to look up at you on a clear night,
        And imagine all the things you've seen.
        You've seen the rise and fall of civilizations,
        And you've witnessed the birth and death of stars.

        You're a witness to history,
        And you're a constant reminder that we are all connected.
        No matter what happens on Earth,
        You're always there, watching over us.

        Thank you, moon, for being there.
        You are a constant source of beauty and inspiration.
        I love you.
        input: write a poem about a man who is lost in a forest
        Detailed  **The Lost Man**

        The lost man wandered through the forest,
        His mind adrift in thought.
        He had been walking for hours,
        And he was starting to lose hope.

        He thought about his family,
        And how worried they must be.
        He thought about his friends,
        And how they would miss him.

        He thought about his life,
        And all the things he had done.
        He thought about his death,
        And how he would never see his loved ones again.

        The lost man stopped walking,
        And he sat down on a rock.
        He closed his eyes,
        And he took a deep breath.

        He thought about the beauty of the forest,
        And the peace that it brought him.
        He thought about the strength of his family and friends,
        And the love that they had for him.

        The lost man opened his eyes,
        And he stood up.
        He smiled,
        And he continued on his journey.

        He knew that he would find his way home,
        Because he was not alone.
        He was surrounded by the love of his family and friends,
        And the beauty of the forest.

        The lost man walked on,
        And he was never lost again.
        input: write a short summary of the book 'the great gatsby'
        Detailed  The Great Gatsby is a novel by F. Scott Fitzgerald that follows the story of Jay Gatsby, a wealthy man who throws lavish parties in an attempt to win back the love of his life, Daisy Buchanan. The novel is set in the Jazz Age on Long Island, and it explores themes of love, loss, and the American Dream.

        The novel begins with Nick Carraway, a young man from the Midwest, moving to New York City to pursue his dream of becoming a writer. He rents a house next door to Gatsby, and he quickly becomes drawn into his world of lavish parties and extravagant wealth.

        Gatsby is a mysterious figure, and Nick is eager to learn more about him. He learns that Gatsby was once a poor boy from the Midwest, but he made his fortune through bootlegging and other illegal activities. He came to New York City with the dream of winning back Daisy, a wealthy young woman whom he had loved in his youth.

        Gatsby throws lavish parties in an attempt to impress Daisy and win her back. He hopes that she will see that he has become a success and that she will fall in love with him again. However, Daisy is already married to Tom Buchanan, a wealthy man from an old-money family.

        Tom and Daisy are a troubled couple. Tom is unfaithful to Daisy, and he is also racist and sexist. Daisy is bored with her marriage and she is attracted to Gatsby's wealth and glamour.

        Gatsby and Daisy eventually begin an affair, but it is doomed from the start. Tom is suspicious of Gatsby and he confronts him. Gatsby is forced to admit that he is not the man that Daisy thought he was.

        Gatsby is eventually killed by George Wilson, a man who believes that Gatsby is having an affair with his wife Myrtle. Gatsby's death is a tragic end to a story of love, loss, and the American Dream.

        The Great Gatsby is a classic American novel that explores the themes of love, loss, and the American Dream. It is a story of a man who will do anything to win back the love of his life, even if it means sacrificing his own happiness. The novel is a powerful reminder that the American Dream is not always what it seems.

        input: what are the different types of cloud computing
        Detailed  There are many different types of cloud computing services, each with its own unique benefits and drawbacks. The most common types of cloud computing services are:

        * **Infrastructure as a Service (IaaS)**: IaaS provides access to computing resources such as servers, storage, and networking, on a pay-as-you-go basis. This is the most basic type of cloud computing service, and it is ideal for businesses that need to quickly and easily scale their IT infrastructure.
        * **Platform as a Service (PaaS)**: PaaS provides a platform for developers to build and deploy applications, without having to worry about the underlying infrastructure. This is ideal for businesses that want to focus on developing their applications, rather than managing their infrastructure.
        * **Software as a Service (SaaS)**: SaaS provides access to software applications that are hosted on the cloud. This is ideal for businesses that want to use software without having to install and maintain it on their own servers.

        In addition to these three main types of cloud computing services, there are also a number of other specialized services available, such as:

        * **Container as a Service (CaaS)**: CaaS provides a platform for developers to build and deploy containerized applications.
        * **Functions as a Service (FaaS)**: FaaS provides a platform for developers to run stateless functions on the cloud.
        * **Machine Learning as a Service (MLaaS)**: MLaaS provides a platform for developers to train and deploy machine learning models.

        The best type of cloud computing service for your business will depend on your specific needs and requirements. If you are unsure which type of service is right for you, it is a good idea to speak to a cloud computing expert.

        Here is a table that summarizes the different types of cloud computing services:

        | Type of Service | Description | Benefits | Drawbacks |
        |---|---|---|---|
        | Infrastructure as a Service (IaaS) | Provides access to computing resources such as servers, storage, and networking, on a pay-as-you-go basis. | **Flexibility** | **Complexity** |
        | Platform as a Service (PaaS) | Provides a platform for developers to build and deploy applications, without having to worry about the underlying infrastructure. | **Rapid development** | **Less control** |
        | Software as a Service (SaaS) | Provides access to software applications that are hosted on the cloud. | **Convenience** | **Dependency** |
        | Container as a Service (CaaS) | Provides a platform for developers to build and deploy containerized applications. | **Isolation** | **Complexity** |
        | Functions as a Service (FaaS) | Provides a platform for developers to run stateless functions on the cloud. | **Scalability** | **Less control** |
        | Machine Learning as a Service (MLaaS) | Provides a platform for developers to train and deploy machine learning models. | **Rapid development** | **Cost** |
        input: {input}
        Detailed """
        
        defaults = {
        'model': 'models/text-bison-001',
        'temperature': 0.65,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.75,
        'max_output_tokens': 1024,
        'stop_sequences': [],
        }

        response = palm.generate_text(
            **defaults,
            prompt=prompt,
        )
        
        return response.result

    def reset(self):
        """Reset the PalmAI instance, allowing re-initialization."""
        self.__class__._instance = None

# Create a singleton instance of PalmAI
palm_ai_instance = PalmAI()