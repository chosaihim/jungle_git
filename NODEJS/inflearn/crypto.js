/**
 * 
 */

var crypto = require("crypto");

var ciphers = crypto.getCiphers();

for(var x of ciphers){
	console.log(x);
}

var key = "test key";
var data = "암호화 할 데이터";

var cipher = crypto.createCipher("aes-256-cbc", key);
var result = cipher.update(data, "utf8", "base64");
result += cipher.final("base64");

console.log("암호화 문자열 :", result);

var decipher = crypto.createDecipher("aes-256-cbc", key);
var result2 = decipher.update(result, "base64", "utf8");
result2 += decipher.final("utf8");

console.log("복호화 문자열 :", result2);