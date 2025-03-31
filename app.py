import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from datetime import datetime, timedelta
from places_api import PlacesAPI

# Load environment variables
load_dotenv()

# Initialize clients
groq_client = Groq(api_key=os.getenv('GROQ_API_KEY'))
places_client = PlacesAPI(api_key=os.getenv('RAPIDAPI_KEY'))


class TravelPlanner:
    def __init__(self):
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {}
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            
    def get_initial_preferences(self):
        """Collect basic travel preferences"""
        st.header("Travel Preferences")
        
        with st.form("travel_basics"):
            destination = st.text_input("Where would you like to go?")
            start_location = st.text_input("Where will you be traveling from?")
            start_date = st.date_input("When do you plan to start your trip?")
            duration = st.number_input("How many days is your trip?", min_value=1, max_value=30, value=7)
            budget = st.selectbox("What's your budget level?", 
                                ["Budget", "Mid-range", "Luxury"])
            purpose = st.multiselect("What's the purpose of your trip?", 
                                   ["Sightseeing", "Relaxation", "Adventure", "Culture", "Food", "Shopping"])
            
            submitted = st.form_submit_button("Continue")
            
            if submitted:
                st.session_state.user_preferences.update({
                    'destination': destination,
                    'start_location': start_location,
                    'start_date': str(start_date),
                    'duration': duration,
                    'budget': budget,
                    'purpose': purpose
                })
                st.session_state.current_step = 1
                st.rerun()

    def get_detailed_preferences(self):
        """Collect detailed preferences"""
        st.header("Additional Preferences")
        
        with st.form("detailed_preferences"):
            dietary = st.multiselect("Dietary Preferences:", 
                                   ["Vegetarian", "Non-Vegetarian", "Vegan", "Halal", "Kosher", "No restrictions"])
            interests = st.multiselect("Specific Interests:", 
                                     ["Museums", "Historical Sites", "Nature", "Local Markets", 
                                      "Nightlife", "Art Galleries", "Local Cuisine"])
            mobility = st.select_slider("Walking Comfort (hours per day):", 
                                      options=[1, 2, 3, 4, 5, 6])
            accommodation = st.selectbox("Accommodation Preference:", 
                                       ["Hostel", "Budget Hotel", "Mid-range Hotel", 
                                        "Luxury Hotel", "Vacation Rental"])
            
            submitted = st.form_submit_button("Generate Itinerary")
            
            if submitted:
                st.session_state.user_preferences.update({
                    'dietary': dietary,
                    'interests': interests,
                    'mobility': mobility,
                    'accommodation': accommodation
                })
                st.session_state.current_step = 2
                st.rerun()

    def get_attractions_for_destination(self, destination: str, interests: list) -> str:
        """Fetch real attractions data using Places API"""
        attractions_data = places_client.get_attractions(destination, interests)
        
        # Format attractions data for the prompt
        attractions_text = "\nReal-time Attractions Information:\n"
        for interest, places in attractions_data.items():
            attractions_text += f"\n{interest.title()} Attractions:\n"
            for place in places:
                attractions_text += f"- {place.get('description', 'No description available')}\n"
        
        return attractions_text

    def generate_itinerary(self):
        """Generate and display the travel itinerary"""
        st.header("Your Personalized Travel Itinerary")
        
        # Show loading message while fetching attractions
        with st.spinner("Fetching real-time attractions data..."):
            attractions_info = self.get_attractions_for_destination(
                st.session_state.user_preferences['destination'],
                st.session_state.user_preferences['interests']
            )
        
        # Convert start date to datetime object
        start_date = datetime.strptime(st.session_state.user_preferences['start_date'], "%Y-%m-%d")
        
        # Generate daily itinerary with specific dates
        itinerary_dates = []
        for i in range(st.session_state.user_preferences['duration']):
            day_date = start_date + timedelta(days=i)
            itinerary_dates.append(day_date.strftime("%B %d, %Y"))

        # Create the prompt for the AI
        system_prompt = """You are an expert travel planner. Generate a detailed day-by-day 
        itinerary based on the user preferences and real-time attractions data. Include:
        - Daily activities with approximate timings
        - Recommended restaurants that match dietary preferences
        - Travel tips and logistics between locations
        - Estimated costs for activities
        Use the provided real attractions data to make the itinerary more accurate and current.
        Format the response in clear markdown with day-by-day breakdown, including specific dates."""

        user_prompt = f"""Create a travel itinerary for:
        Destination: {st.session_state.user_preferences['destination']}
        Start Date: {st.session_state.user_preferences['start_date']}
        Duration: {st.session_state.user_preferences['duration']} days
        Budget Level: {st.session_state.user_preferences['budget']}
        Interests: {', '.join(st.session_state.user_preferences['interests'])}
        Dietary Preferences: {', '.join(st.session_state.user_preferences['dietary'])}
        Walking Comfort: {st.session_state.user_preferences['mobility']} hours per day
        Accommodation: {st.session_state.user_preferences['accommodation']}

        {attractions_info}

        Format the itinerary with specific dates, like:
        Day 1 ({itinerary_dates[0]}): Arrival and Activities
        Day 2 ({itinerary_dates[1]}): Exploration
        ..."""
        
        # Generate itinerary using Groq
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        
        # Display the itinerary
        st.markdown(response.choices[0].message.content)
        
        # Simplified download button (removed the columns and second button)
        st.download_button(
            label="Download Itinerary",
            data=response.choices[0].message.content,
            file_name="travel_itinerary.txt",
            mime="text/plain"
        )

    def main(self):
        st.title("AI Travel Planner")
        
        if st.session_state.current_step == 0:
            self.get_initial_preferences()
        elif st.session_state.current_step == 1:
            self.get_detailed_preferences()
        elif st.session_state.current_step == 2:
            self.generate_itinerary()
            if st.button("Start Over"):
                st.session_state.current_step = 0
                st.session_state.user_preferences = {}
                st.rerun()

if __name__ == "__main__":
    planner = TravelPlanner()
    planner.main()
