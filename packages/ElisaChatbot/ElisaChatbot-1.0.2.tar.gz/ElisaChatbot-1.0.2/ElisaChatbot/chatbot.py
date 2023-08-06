from requests import get

class Elisa():
    def __init__(self):
        self.url = 'https://some1hing.pythonanywhere.com/chatbot'

    def elisa(self, query):
        try:
            url = f"{self.url}/{query}"
            response = get(url).json()["response"]
            return str(response)
        except:
            return "ERROR!! Elisa Chatbot not responding."