package com.example.pic_pho.WifiDirect

import android.app.IntentService
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.util.Log
import com.google.gson.JsonObject
import java.io.*
import java.net.InetSocketAddress
import java.net.Socket


// 인텐트 받아서 stream에 태워보내는 클래스
class SendStreamIntentService : IntentService("SendStreamIntentService") {

    // 인텐트 받아서 처리해주는 함수
    override fun onHandleIntent(intent: Intent?) {
        val context: Context = applicationContext
        val cr = context.contentResolver
        var socket = Socket()
        Log.d(TAG, "IntentService Start")

        when (intent!!.action) {

            // Client가 Server에게 사진을 선택하고 서버에 전송 (Protocol 2)
            ACTION_CONNECT_TO_SERVER -> {

                // sendToServerPhotos 함수에서 넘어온 Intent에서 프로퍼티 추출
                val protocol = intent.extras!!.getString(EXTRAS_PROTOCOL)
                val host = intent.extras!!.getString(EXTRAS_GROUP_OWNER_IP)
                val uri = intent.extras!!.getString(EXTRAS_URI)
                val photoOwnerMac = intent.extras!!.getString(EXTRAS_PHOTO_OWNER_MAC)

                val port = intent.extras!!.getInt(EXTRAS_GROUP_OWNER_PORT)
                val status = intent.extras!!.getInt(EXTRAS_SEND_STATUS)
                val clientPhotoCount = intent.extras!!.getInt(EXTRAS_CLIENT_PHOTO_COUNT)
                val clientPhotoDigit = intent.extras!!.getInt(EXTRAS_CLIENT_PHOTO_DIGIT)

                // 통신을 위한 MetaData JsonObejct 로 변환
                var jsonObject = JsonObject()
                jsonObject.addProperty("photoOwnerMac", photoOwnerMac)
                jsonObject.addProperty("status", status)
                jsonObject.addProperty("clientPhotoCount", clientPhotoCount)

                // Server와 소켓 통신 시작
                val socketAddress = InetSocketAddress(host.toString(), port)

                try {
                    // 소켓 및 Stream 생성
                    socket.connect(socketAddress, SOCKET_TIMEOUT)
                    var outputStream = socket.getOutputStream()
                    Log.d(TAG, "Socket Connect Success")


                    // protocol 전달 (Header 부분 시작)
                    outputStream.write(protocol!!.encodeToByteArray())

                    // 사진의 총 갯수의 자릿수를 전달
                    outputStream.write(clientPhotoDigit.toString().encodeToByteArray())

                    // Json(Meta Data) 전송 (Header 부분 종료)
                    var stringjson: ByteArray = jsonObject.toString().encodeToByteArray()
                    outputStream.write(stringjson)

                    // File을 input에 저장하고, OutStream으로 전송 (File 전송)
                    var input = cr.openInputStream(Uri.parse(uri.toString()))
                    input!!.copyTo(outputStream)

                    socket.close()

                } catch (e: IOException) {
                    Log.d(TAG, "Socket Connect failed")
                    socket.close()
                }
            }

            // Peer가 GroupOwner에게 짧은 핸드쉐이킹용 통신 (Protocol 1, 3)
            ACTION_FIRST_CONNECT -> {
                val protocol = intent.extras!!.getString(EXTRAS_PROTOCOL)
                val host = intent.extras!!.getString(EXTRAS_GROUP_OWNER_IP)
                val port = intent.extras!!.getInt(EXTRAS_GROUP_OWNER_PORT)

                val socketAddress = InetSocketAddress(host.toString(), port)

                try {
                    socket.connect(socketAddress, SOCKET_TIMEOUT)
                    var outputStream = socket.getOutputStream()
                    outputStream.write(protocol!!.encodeToByteArray())
                    socket.close()

                } catch (e: IOException) {
                    socket.close()
                    e.printStackTrace()
                }
            }
        }
    }

    companion object {
        private const val TAG = "SendStreamIntentService"
        private val SOCKET_TIMEOUT = 5000
        val ACTION_CONNECT_TO_SERVER = "com.example.picpho.CONNECT_TO_SERVER"
        val ACTION_FIRST_CONNECT = "com.example.picpho.FIRST_CONNECT" //todo : 변수 이름 변경 필요
        val EXTRAS_GROUP_OWNER_IP = "serverIP"
        val EXTRAS_GROUP_OWNER_PORT = "serverPort"
        val EXTRAS_URI = "uri"
        var EXTRAS_SEND_STATUS = "status"
        val EXTRAS_PHOTO_OWNER_MAC = "photoOwnerMac"
        val EXTRAS_PROTOCOL = "protocol"
        val EXTRAS_CLIENT_PHOTO_COUNT = "clientPhotoCount"
        val EXTRAS_CLIENT_PHOTO_DIGIT = "clientPhotoDigit"
    }
}