/**
 * 
 */

var crypto = require("crypto");

// 지원되는 암호화 알고리즘 보기
var ciphers = crypto.getCiphers(); 

// 출력
for(var x of ciphers){
	console.log(x);
}

var key = "test key"; // key 가 있어야 나중에 암호화 된 데이터를 다시 풀 수 있음
var data = "암호화 할 데이터";

// 암호화용 객체 생성
var cipher = crypto.createCipher("aes-256-cbc", key); //(암호화 방식, key)
var result = cipher.update(data, "utf8", "base64");//(암호화할 데이터, 어떠한 양식의 값을, 어떠한 양식으로 암호화)
                                                    // 문자의 경우 utf8
result += cipher.final("base64");   //result 안에 암호화 할 문자열을 넣어줌

console.log("암호화 문자열 :", result);

var decipher = crypto.createDecipher("aes-256-cbc", key);
var result2 = decipher.update(result, "base64", "utf8"); // 암호화와 반대로 
result2 += decipher.final("utf8");

console.log("복호화 문자열 :", result2);