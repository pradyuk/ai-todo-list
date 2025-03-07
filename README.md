Install dependencies.
```
pip install -r requirements.txt
cp env.sample .env
cd frontend
npm install
cd ..
```

Run backend:
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
