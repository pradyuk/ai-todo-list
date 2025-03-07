Install dependencies.
```
pip install -r requirements.txt
cp env.sample .env
cd frontend
npm install
cd ..
```

Run backend:
First update the .env file with the OpenAPI key
```
./manage.py migrate
./manage.py runserver
```

Create superuser:
```
./manage.py createsuperuser
```

Run frontend:
```
cd frontend
npm run dev
```

Run task accomplishing agent:
```
./manage.py accomplish_task
```

Frontend URL:
```
http://localhost:5173/
```

Admin URL:
```
http://localhost:8000/admin/
```

Run eval script (make sure the agent is not running):
```
./manage.py eval
```
