package com.example.pic_pho.WifiDirect

import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.media.MediaScannerConnection
import android.net.Uri
import android.util.Log
import com.example.pic_pho.PhotoRoom.PhotoRoomActivity
import org.json.JSONObject
import java.io.File
import java.io.FileOutputStream
import java.net.Socket
import java.util.*

// FileReceiveServerAsyncTask가 생성한 thread
// SendStreamIntentService로부터 Stream을 받아서 파일을 복사하는 thread
class FileReceiveActionThread(var client: Socket, var context: Context) : Thread() {

    override fun run() {
        super.run()
        Log.d(TAG, "FileReceiverAction Start")
        var inputStream = client.getInputStream()
        var peersIP = client.inetAddress.hostName

        // Protocol number 획득
        var protocolByteArray = ByteArray(1)
        inputStream.read(protocolByteArray)

        Log.d(TAG, "run: String(protocolByteArray, Charsets.UTF_8 ${String(protocolByteArray, Charsets.UTF_8)}")

        when(String(protocolByteArray, Charsets.UTF_8)){

            // Protocol 1 : Peer가 GroupOwner에게 처음 접속할 때 보내는 핸드쉐이킹 (Peer IP 저장)
            "1" -> {
                if(!WifiDirectMainActivity.connectedPeerList.contains(peersIP)) {
                    WifiDirectMainActivity.connectedPeerList.add(peersIP)
                    WifiDirectMainActivity.connectedPeerMap.set(peersIP, 0)
                }
                Log.d(TAG, "FileReceiveActionThread 접속 중인 피어 수 : ${WifiDirectMainActivity.connectedPeerList.size}")
            }

            // Protocol 2 : Client가 Server에게 사진을 전송할 때 사용하는 프로토콜
            "2" -> {
                // 유저가 보낸 사진 개수의 자리수를 카운트하고, ByteArray 크기를 조정한다
                var photoDigitByteArray = ByteArray(1)
                inputStream.read(photoDigitByteArray)
                var readByteArraySize = 69
                when (String(photoDigitByteArray, Charsets.UTF_8)) {
                    "2" -> {
                        readByteArraySize = 70
                    }
                    "3" -> {
                        readByteArraySize = 71
                    }
                }

                // meta data 획득
                var byteArray = ByteArray(readByteArraySize)
                var testSize: Int = inputStream.read(byteArray)
                Log.d(TAG, "run: testSize is === $testSize")
                var metaData = String(byteArray, Charsets.UTF_8)
                val jsonObject = JSONObject(metaData)
                var status = Integer.parseInt(jsonObject.get("status").toString())
                var photoOwnerMac = jsonObject.get("photoOwnerMac")
                var clientPhotoCount =
                    Integer.parseInt(jsonObject.get("clientPhotoCount").toString())

                Log.d(TAG, "stringjson receive: ${jsonObject}")

                // unique한 파일 이름 만들어줌
//                var filename: String =
//                    "/storage/emulated/0" + "/DCIM/Picpho/" + System.currentTimeMillis() + ".jpg"

                // 현재 날짜 구하기
                val calendar:Calendar = Calendar.getInstance()
                val year = calendar.get(Calendar.YEAR)
                val mon = calendar.get(Calendar.MONTH)
                val day = calendar.get(Calendar.DAY_OF_MONTH)

                var filename: String =
                    "/sdcard/DCIM/Picpho/" + "${year}+${mon}+${day}"+"_"+System.currentTimeMillis() + ".jpg"

                var file = File(filename)
                Log.d(TAG, "받았을 때 URI" + file.toString())

                // 넘겨받은 Meta Data로 photoInfo 객체를 만들어 리스트에 저장
                var photoinfo = PhotoInfo(
                    Uri.parse(filename),
                    photoOwnerMac.toString(),
                    client.inetAddress.hostName
                )

                Log.d(TAG, "run: Photoinfo : ${photoinfo}")

                WifiDirectMainActivity.photoInfoList.add(photoinfo)

                // 디렉토리 존재하지 않으면 디렉토리 생성
                val dirs = File(file!!.parent.toString())
                if (!dirs.exists()) dirs.mkdirs()

                // 실제로 파일 복사하는 부분
                if (file!!.createNewFile()) {
                    var byteSize = inputStream.copyTo(FileOutputStream(file))
                    Log.d(TAG, "After copyTo 받는 쪽 파일 크기 : ${byteSize}")
                    scanFile(context, file!!, "jpg")
                    Log.d(TAG, "FileReceiverAction Finished")
                }

                var groupMemberCount = WifiDirectMainActivity.groupMemberCount
                Log.d(TAG, "run: status ----- $status")


                // status == 1 인 경우, GO가 해당 Peer로부터 모든 사진을 전송 받았음을 인지
                if (status == 1) {
                    if (WifiDirectMainActivity.isGroupOwner) {
                        WifiDirectMainActivity.sentPhotoCount++
//                        WifiDirectMainActivity.textViewShowGroupCount!!.text =
//                            "Member : ${WifiDirectMainActivity.groupMemberCount}" + "Sent : ${WifiDirectMainActivity.sentPhotoCount}"

                        // 해당 Peer가 보낼 사진의 수를 Map에 저장한다
                        if (WifiDirectMainActivity.connectedPeerMap.get(peersIP) == 0) {
                            WifiDirectMainActivity.connectedPeerMap[peersIP] = clientPhotoCount
                        }

                        if (groupMemberCount != 0 && groupMemberCount == WifiDirectMainActivity.sentPhotoCount) {
                            Log.d(TAG, "모든 Peer 전송 완료")
                            // 모든 Peer에게서 사진을 받은 경우, 버튼 활성화
                            WifiDirectMainActivity.uiHandler.post {
                                WaitingForOwnerActivity.wifiChoosePhotoCardView!!.isEnabled = true
                                WaitingForOwnerActivity.wifiChoosePhotoCardView!!.setCardBackgroundColor(
                                    Color.parseColor("#76CBFF"))
                            }
                        }
                    }

                    // status == 2 인 경우, GO로 부터 Peer가 사진 전송을 받았음을 인지함
                } else if (status == 2) {
                    Log.d(TAG, "FileReceiverAction, 서버에서 사진 내꺼 빼고 다 받음")
                    var intent = Intent(context, PhotoRoomActivity::class.java)
                    context.startActivity(intent)
                    sleep(1000)
                    client.close()
                }
            }

            // GroupOwner가 Peer에게 보낼 사진이 없을 경우
            "3" -> {
                Log.d(TAG, "run: Server에서 프로토콜 3 받음, Photolist size = ${WifiDirectMainActivity.photoInfoList.size}")
                var intent = Intent(context, PhotoRoomActivity::class.java)
                context.startActivity(intent)
                sleep(1000)
                client.close()
            }
        }
    }

    companion object {
        private const val TAG = "FileReceiveAction"

        // 전송된 파일을 갤러리앱에서 볼 수 있도록 scan해주는 함수
        fun scanFile(context: Context?, f: File, mimeType: String) {
            MediaScannerConnection
                .scanFile(context, arrayOf(f.absolutePath), arrayOf(mimeType), null)
        }
    }
}


