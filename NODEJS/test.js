const nodemailer = require('nodemailer');
const email = {
    "host": "smtp.mailtrap.io",
    "port": 2525,
    "secure": false,
    "auth":{
        "user": "",//"82e975b2fa894a",
        "pass": "",//"ce751d6a98d2e7",
    }
};

const send = async(option) => {
    nodemailer.createTransport(email).sendMail(option, (error, info)=>{
        if(erorr){
            console.log(error);
        }else{
            console.log(info);
            return info.response;
        }
    });
};

let email_data = {
    from: 'chosaihim@gmail.com',
    to: 'chosaihim@gmail.com',
    subject: '테스트 메일 입니다.',
    text: 'node.js. 한시간'
}

send(email_data);