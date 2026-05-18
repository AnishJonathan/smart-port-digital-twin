import os
os.environ['WEATHERAPI_KEY'] = '4e7c491ad8c5473584042531261805'
from app import create_app

app = create_app()

with app.app_context():
    from flask import url_for
    with app.test_client() as client:
        # We want to see the stack trace, not the 500.html template.
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        
        # Bypass login by setting a session
        with client.session_transaction() as sess:
            sess['_user_id'] = '1'
            sess['_fresh'] = True
            
        try:
            response = client.get('/dashboard/')
            print("Status Code:", response.status_code)
            if response.status_code == 500:
                print("500 Error encountered!")
                print(response.data.decode('utf-8'))
        except Exception as e:
            import traceback
            traceback.print_exc()
