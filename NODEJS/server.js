const express = require('express');
const app = express();

const server = app.listen(3000,()=>{
    console.log('Start Server: localhost:3000');
});

//! html 페이지 렌더링 하기 위해 setting
app.set('views', __dirname + '/views');
app.set('view engine', 'ejs');
app.engine('html',require('ejs').renderFile);


app.get('/', function(req, res){
    res.render('index.html');
    // res.send('hello world');
})

app.get('/about', function(req, res){
    res.send('about page');
})

//! DB를 사용하기 위해서 먼저 연동하기
// 마리아 db는 mysql에서 파생된 db 이기 때문에 
// mysql 설치하면 둘 다 사용할 수 있음
//? 여기 이제 정보들은 실제 username이랑 password같은거 써야함.
var mysql = require('mysql');
var pool  = mysql.createPool({
  connectionLimit : 10,
  host            : 'example.org',
  user            : 'bob',
  password        : 'secret',
  database        : 'my_db'
});

//? 위의 db 풀을 갖고
//? 아래 getConnection으로 커넥션 연결하기
app.get('/db', function(req, res){
    pool.getConnection(function(err, connection) {
        if (err) throw err; // not connected!
       
        // Use the connection
        connection.query('select * from Test', function (error, results, fields) { //?Test table에 있는 정보를 전부 가져온다.
            res.send(JSON.stringify(results)); //?
            console.log('results',results);
          // When done with the connection, release it.
          connection.release();
       
          // Handle error after the release.
          if (error) throw error;
       
          // Don't use the connection here, it has been returned to the pool.
        });
      });
})