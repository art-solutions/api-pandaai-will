import os
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from pandasai import SmartDataframe
from pandasai.connectors import PostgreSQLConnector
import pandasai as pai

def clear_cache():
    """Clear the cache of the pandasai library."""
    pai.clear_cache()

app = Flask(__name__)

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = ""

# Initialize the OpenAI chat model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # Or another OpenAI chat model
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

# PostgreSQL connector configurationhttps://idx.google.com/pythonsearch-4704807
postgres_connector = PostgreSQLConnector(
    config={
        "host": "192.168.1.84",
        "port": 5432,
        "database": "postgres",
        "username": "postgres",
        "password": "postgres",
        "table": "testlang"
    }
)
import traceback

@app.route('/postgresql', methods=['POST'])
def postgresql_api():
    try:
        # Create a SmartDataframe instance for each request
        df = SmartDataframe(postgres_connector, config={"llm": llm})

        prompt = request.json['prompt']
        result = df.chat(prompt)
        print("Result:")
        print(result)

        # Close the cache connection after each request
        #df.get_cache().connection.close()

        # Convert result to string
        result_str = str(result)

        return jsonify({'result': result_str})
    except Exception as e:
        print("Error:")
        print(str(e))
        print("Traceback:")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(port=5555, debug=False)
