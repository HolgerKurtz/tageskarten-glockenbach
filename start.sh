# For development use (simple logging, etc):
pip3 install -r requirements.txt
/usr/bin/python3 server.py
# For production use: 
# gunicorn server:app -w 1 --log-file -