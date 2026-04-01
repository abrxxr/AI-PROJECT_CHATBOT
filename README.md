# AI Chatbot with LLM Integration

This is an AI chatbot built with Flask that uses OpenAI's GPT model to generate responses to user inputs.

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Get an OpenAI API key from [OpenAI](https://platform.openai.com/api-keys)

3. Create a `.env` file in the project root and add your API key:
   ```
   OPENAI_API_KEY=your-actual-api-key-here
   ```

## Running the Application

1. Start the Flask server:
   ```bash
   python server.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Sign up or sign in, then navigate to the chat interface.

## Features

- User registration and authentication
- Dynamic chatbot responses using OpenAI's GPT-3.5-turbo
- Chat history persistence during session
- Responsive web interface

## How it works

The chatbot now uses OpenAI's LLM to generate responses based on user input. It can handle any type of query and provide relevant answers based on keywords and context in the user's message.

## Note

Make sure to keep your OpenAI API key secure and never commit it to version control.