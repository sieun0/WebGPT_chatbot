// server.js
const http = require('http');
const fs = require('fs');
const ejs = require('ejs');

const server = http.createServer((req, res) => {
  if (req.url === '/') {
    // HTML 파일 읽기
    fs.readFile('chat.html', 'utf8', (err, html) => {
      if (err) {
        res.statusCode = 500;
        res.end('Internal Server Error');
        return;
      }

      // 클라이언트로 HTML 파일 전송
      res.setHeader('Content-Type', 'text/html');
      res.end(html);
    });
  } else if (req.url === '/send-message') {
    if (req.method === 'POST') {
      let body = '';
      req.on('data', (chunk) => {
        body += chunk.toString();
      });
      req.on('end', () => {
        // 전송된 메시지에서 inputText 값 추출
        const inputText = decodeURIComponent(body.split('=')[1]);

        // inputText 값 사용하여 처리
        // 응답 데이터 생성
        const responseData = {
          message: 'Message received',
        };

        // JSON 형식으로 응답
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(responseData));
      });
    } else {
      res.statusCode = 405;
      res.end('Method Not Allowed');
    }
  } else {
    // 다른 요청에 대한 처리
    res.statusCode = 404;
    res.end('Not Found');
  }
});

server.listen(3000, () => {
  console.log('Server is running on port 3000');
});
