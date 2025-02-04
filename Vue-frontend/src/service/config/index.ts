const TIME_OUT = 10000;

let BASE_URL = 'https://django-backend-main-dde75ed28e39.herokuapp.com/';
if (import.meta.env.MODE === 'production') {
  BASE_URL = 'https://django-backend-main-dde75ed28e39.herokuapp.com/'; // a temp test url(@lipeng) provide login validate
} else {
  BASE_URL = 'http://localhost:8000'; // a temp test url(@lipeng) provide login validate
}

export { BASE_URL, TIME_OUT };
