import requests

class Tests:
    
   def test_perform_login_api(self):
      response = requests.get('https://weatherdbi.herokuapp.com/data/weather/cluj')
      assert response.status_code == 200