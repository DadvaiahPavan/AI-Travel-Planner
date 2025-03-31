# AI Travel Planner

An intelligent travel planning application that generates personalized travel itineraries using AI and real-time attraction data. The application combines Groq's LLM capabilities with Google Maps Places API to create detailed, context-aware travel plans.

## Features

- **Multi-step Travel Planning Process**
  - Basic travel preferences collection
  - Detailed preferences and interests gathering
  - Real-time attraction data integration
  - AI-powered itinerary generation

- **Smart Preference Collection**
  - Destination and dates
  - Budget level preferences
  - Trip duration planning
  - Dietary requirements
  - Activity interests
  - Mobility considerations
  - Accommodation preferences

- **Real-time Data Integration**
  - Integration with Google Maps Places API
  - Up-to-date attraction information
  - Location-based recommendations
  - Smart place suggestions based on user interests

- **AI-Powered Itinerary Generation**
  - Day-by-day detailed schedules
  - Time-specific activity planning
  - Restaurant recommendations based on dietary preferences
  - Travel tips and logistics
  - Cost estimates for activities

## Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Groq (llama3-8b-8192 model)
- **APIs**: 
  - Google Maps Places API (via RapidAPI)
  - Groq API
- **Language**: Python 3.x

## Prerequisites

- Python 3.x
- Groq API key
- RapidAPI key (for Google Maps Places API)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-travel-planner
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your API keys: 