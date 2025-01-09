import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define the items and their corresponding Big Five traits with positive phrasing
items = [
    # Extraversion (Factor 1)
    ("I feel energized in social situations.", 1, True),
    ("I prefer spending time with others rather than being alone.", 1, True),
    ("I enjoy connecting with new people.", 1, True),
    ("I find it easy to initiate conversations.", 1, True),
    ("I feel confident and at ease in social gatherings.", 1, True),
    ("I actively seek out opportunities to interact with others.", 1, True),
    ("I enjoy quiet moments and personal space.", 1, False),
    ("I feel comfortable and happy around others.", 1, True),
    ("I am content with smaller social circles.", 1, False),
    ("I prefer calm environments over crowded settings.", 1, False),

    # Agreeableness (Factor 2)
    ("I genuinely care about others' well-being.", 2, True),
    ("I value helping others whenever I can.", 2, True),
    ("I take time to listen and understand people’s feelings.", 2, True),
    ("I find joy in assisting others in need.", 2, True),
    ("I believe in the importance of kindness and cooperation.", 2, True),
    ("I work well in team settings and support group harmony.", 2, True),
    ("I am mindful of other people's needs and emotions.", 2, True),
    ("I like to foster positive relationships with others.", 2, True),
    ("I actively help resolve conflicts and maintain peace.", 2, True),
    ("I enjoy being empathetic and compassionate towards others.", 2, True),

    # Conscientiousness (Factor 3)
    ("I always try to stay organized and plan ahead.", 3, True),
    ("I take pride in being responsible and dependable.", 3, True),
    ("I find satisfaction in completing tasks on time.", 3, True),
    ("I consistently keep my commitments and promises.", 3, True),
    ("I pay attention to details to ensure the quality of my work.", 3, True),
    ("I enjoy taking proactive steps to achieve my goals.", 3, True),
    ("I prefer to keep things flexible and spontaneous.", 3, False),
    ("I like to maintain order and structure in my surroundings.", 3, True),
    ("I enjoy staying on top of my responsibilities and projects.", 3, True),
    ("I tend to work hard and focus on achieving results.", 3, True),

    # Neuroticism (Factor 4)
    ("I tend to stay calm and composed even in stressful situations.", 4, True),
    ("I feel confident in handling challenges that come my way.", 4, True),
    ("I feel emotionally stable and resilient in difficult circumstances.", 4, True),
    ("I tend to approach stressful situations with a positive attitude.", 4, True),
    ("I am able to manage my emotions effectively and stay balanced.", 4, True),
    ("I handle pressure well and stay focused on solutions.", 4, True),
    ("I am usually able to stay relaxed and positive.", 4, True),
    ("I maintain a sense of control when faced with adversity.", 4, True),
    ("I feel secure and resilient, even when challenges arise.", 4, True),
    ("I rarely let my emotions take over in stressful situations.", 4, True),

    # Openness to Experience (Factor 5)
    ("I enjoy exploring new ideas and possibilities.", 5, True),
    ("I am curious and eager to learn about the world around me.", 5, True),
    ("I value creativity and enjoy thinking outside the box.", 5, True),
    ("I embrace new experiences and welcome the unknown.", 5, True),
    ("I enjoy discovering different perspectives and learning from others.", 5, True),
    ("I am open to trying new things and embracing change.", 5, True),
    ("I appreciate abstract and philosophical ideas.", 5, True),
    ("I find joy in exploring diverse cultures and lifestyles.", 5, True),
    ("I enjoy thinking about and imagining different futures.", 5, True),
    ("I often find myself considering new possibilities for growth.", 5, True),
]

# Initialize session state variables
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "responses" not in st.session_state:
    st.session_state.responses = [None] * len(items)
if "scores" not in st.session_state:
    st.session_state.scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

# Helper functions
def next_question(response):
    # Save the response and calculate score
    idx = st.session_state.current_index
    question, factor, positive = items[idx]
    score = response if positive else 6 - response
    st.session_state.responses[idx] = response
    st.session_state.scores[factor] += score
    # Move to the next question
    if st.session_state.current_index < len(items) - 1:
        st.session_state.current_index += 1
    else:
        st.session_state.finished = True  # Flag to indicate that all questions are finished

def previous_question():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

# Function to plot radar chart
def plot_radar_chart(scores):
    labels = ['Extraversion', 'Agreeableness', 'Conscientiousness', 'Neuroticism', 'Openness to Experience']
    values = [scores[1], scores[2], scores[3], scores[4], scores[5]]

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.plot(angles, values, color='blue', linewidth=2)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    st.pyplot(fig)

# Display introductory message
if "started" not in st.session_state:
    st.title("🌟 Big Five Personality Test 🌟")
    st.write(
        """
        Welcome to the Big Five Personality Test! 🌈
        
        This test is designed to help you better understand your unique personality traits. The five factors measured are:
        1. **Extraversion**: How social and outgoing you are.
        2. **Agreeableness**: How cooperative and empathetic you are.
        3. **Conscientiousness**: How organized and responsible you are.
        4. **Neuroticism**: How well you handle stress and challenges.
        5. **Openness to Experience**: How curious and creative you are.

        Each question asks you to reflect on certain aspects of your personality. You will rate your responses from 1 (Strongly Disagree) to 5 (Strongly Agree).

        **Start the test by clicking the button below!**
        """
    )
    if st.button("Start Test"):
        st.session_state.started = True
        st.session_state.current_index = 0  # Start the test from the first question

# Once the test has started
if "started" in st.session_state and st.session_state.started:
    if "finished" not in st.session_state or not st.session_state.finished:
        if st.session_state.current_index < len(items):
            idx = st.session_state.current_index
            question, factor, positive = items[idx]
            st.write(f"### Question {idx + 1} of {len(items)}")
            st.markdown(f"**{question}**")

            col1, col2, col3, col4, col5 = st.columns(5)
            if col1.button("Strongly Disagree"):
                next_question(1)
            if col2.button("Disagree"):
                next_question(2)
            if col3.button("Neutral"):
                next_question(3)
            if col4.button("Agree"):
                next_question(4)
            if col5.button("Strongly Agree"):
                next_question(5)

            # Navigation buttons
            if st.session_state.current_index > 0:
                if st.button("⬅️ Previous"):
                    previous_question()
    else:
        # Before showing the result, ask for a smile photo
        st.write("### 😊 Please smile and take a photo to proceed to the results!")
        image = st.camera_input("Take a picture (Smile!)")

        if image is not None:
            # If an image is taken, show the results
            plot_radar_chart(st.session_state.scores)

            # Display the results
            st.write("### Your Big Five Personality Scores 🧠")
            st.write(f"**Extraversion**: {st.session_state.scores[1]} 😎")
            st.write(f"**Agreeableness**: {st.session_state.scores[2]} 🤝")
            st.write(f"**Conscientiousness**: {st.session_state.scores[3]} 📅")
            st.write(f"**Neuroticism**: {st.session_state.scores[4]} 😥")
            st.write(f"**Openness to Experience**: {st.session_state.scores[5]} 🌱")

            # Interpretation and advice for each factor
            st.write("### 📝 Detailed Interpretation and Advice")

            # Extraversion Interpretation
            if st.session_state.scores[1] > 35:
                st.write("**Extraversion**: You're a vibrant and sociable person who thrives in social situations. Keep embracing your energy and passion! 🌟")
            elif st.session_state.scores[1] > 25:
                st.write("**Extraversion**: You enjoy meaningful interactions but also appreciate quiet time. Balance is key! ⚖️")
            else:
                st.write("**Extraversion**: You value personal space and find peace in solitude. Continue nurturing your inner calm. 🏡")

            # Agreeableness Interpretation
            if st.session_state.scores[2] > 35:
                st.write("**Agreeableness**: You are deeply compassionate, always looking out for others. Keep spreading kindness and harmony. 💖")
            elif st.session_state.scores[2] > 25:
                st.write("**Agreeableness**: You find a great balance between cooperation and assertiveness. Keep nurturing your relationships. 🏆")
            else:
                st.write("**Agreeableness**: You value independence and assertiveness. Your determination is a strength! ⚔️")

            # Conscientiousness Interpretation
            if st.session_state.scores[3] > 35:
                st.write("**Conscientiousness**: You are highly disciplined and organized. Keep up the great work, as your dedication is paying off. 📈")
            elif st.session_state.scores[3] > 25:
                st.write("**Conscientiousness**: You are flexible yet responsible. Find opportunities to maintain balance in both structure and spontaneity. 🧳")
            else:
                st.write("**Conscientiousness**: You prefer a more relaxed approach. Embrace your creative side and continue developing your organizational skills. 💡")

            # Neuroticism Interpretation
            if st.session_state.scores[4] > 35:
                st.write("**Neuroticism**: You handle stress with ease and are emotionally stable. Keep practicing mindfulness for even more balance. 🧘‍♂️")
            elif st.session_state.scores[4] > 25:
                st.write("**Neuroticism**: You handle pressure well but may experience occasional fluctuations. Focus on mindfulness techniques to stay grounded. 🍃")
            else:
                st.write("**Neuroticism**: You may feel more emotional at times. Focus on practices that support your emotional well-being. 🛑")

            # Openness to Experience Interpretation
            if st.session_state.scores[5] > 35:
                st.write("**Openness to Experience**: You are creative and innovative. Keep seeking new adventures and stay curious! 🎨")
            elif st.session_state.scores[5] > 25:
                st.write("**Openness to Experience**: You appreciate creativity while valuing practicality. Seek opportunities to combine the best of both worlds. ⚙️")
            else:
                st.write("**Openness to Experience**: You prefer tradition and familiarity. Embrace new ideas to continue growing. 🛠️")
