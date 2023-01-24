var dns = require('dns');

// dns 서버가 언제 값을 돌려줄지 모르기 때문에 기다리고 있다가,
// 값을 도려주면 function 실행
dns.lookup("google.com", function(err, address, family) {
    // 주소가 ipv4 일지 ipv6 일지는 모름 대부분 4
    console.log("IP 주소: ", address);
    console.log("IP 버전: ", family);
});
