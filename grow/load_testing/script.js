import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  const url = 'http://localhost:8000/shortie';
  const payload = JSON.stringify(
    {
      "alias": "conginuadau",
      "origin_url": "https://gg_test.com/"
    }
  );

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  http.post(url, payload, params);
  sleep(1);
}
