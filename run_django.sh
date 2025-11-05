docker run -it \
  -v "$(pwd):/usr/src/app" \
  -w /usr/src/app \
  -p 8000:8000 \
  coderr \
  python manage.py runserver 0.0.0.0:8000