package com.example.pic_pho

import android.Manifest
import android.app.Dialog
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.Gravity
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.pic_pho.CellularSocket.SocketUtill
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.WifiDirect.SendStreamIntentService
import com.github.nkzawa.socketio.client.Socket
import com.google.firebase.iid.FirebaseInstanceId
import com.kakao.sdk.auth.model.OAuthToken
import com.kakao.sdk.common.model.AuthErrorCause.*
import com.kakao.sdk.user.UserApiClient
import kotlinx.android.synthetic.main.activity_login.*
import java.security.MessageDigest

class LoginActivity : AppCompatActivity() {
    private val TAG = "LoginActivity"
    lateinit var mSocket: Socket;

    //친구 초대 받았을 때
    lateinit var intentfromfirebase: Intent // = getIntent()

    companion object{
        var roomAddress: String?= null

    }

    @RequiresApi(Build.VERSION_CODES.P)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)


        //일단 초대 받은거면 방 번호를 받아둔다.
        roomAddress = null
        intentfromfirebase = getIntent()
        if (intentfromfirebase != null) {
            roomAddress = intentfromfirebase.extras?.getString("RoomAddress")
            Toast.makeText(this, "${roomAddress}", Toast.LENGTH_SHORT).show()
//            if (roomAddress != null) {
//                UserApiClient.instance.accessTokenInfo { tokenInfo, error ->
//                    if (error != null) {
//                        Toast.makeText(this, "초대 받았으나 로그인 되어있지 않음.", Toast.LENGTH_SHORT).show()
//
//                    } else if (tokenInfo != null) {
////                      Toast.makeText(this, "토큰 정보 보기 성공", Toast.LENGTH_SHORT).show()
//                        Toast.makeText(this, "${roomAddress}", Toast.LENGTH_SHORT).show()
//                        Log.d(TAG, "onCreate: ${roomAddress}")
//                        var photoroomIntent: Intent =
//                            Intent(this, ServerPhotoRoomActivity::class.java)
//                        startActivity(photoroomIntent)
//                    }
//                }
//
//            }
        }

        requestPermissionToUser() //todo : Wifi 사용 중인지 점검하는 퍼미션 체크 필요


        UserApiClient.instance.accessTokenInfo { tokenInfo, error ->
            if (error != null) {
//                Toast.makeText(this, "토큰 정보 보기 실패", Toast.LENGTH_SHORT).show()
            } else if (tokenInfo != null) {
                Toast.makeText(this, "토큰 정보 보기 성공, 방번호: ${roomAddress}", Toast.LENGTH_SHORT).show()

                if(roomAddress.isNullOrEmpty()){
                    val intent = Intent(this, SelectP2pOrServerActivity::class.java)
                    startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
                }
                else{
                    val intent = Intent(this, ServerPhotoRoomActivity::class.java)
                    intent.putExtra("roomAddress",roomAddress )
                    startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
                }
            }
        }

//        getHash() //디버깅용 해시 얻는 함수
        val callback: (OAuthToken?, Throwable?) -> Unit = { token, error ->

            if (error != null) {
                Log.d(TAG, "token ${token} error ${error}")
                when {
                    error.toString() == AccessDenied.toString() -> {
                        Toast.makeText(this, "접근이 거부 됨(동의 취소)", Toast.LENGTH_SHORT).show()
                    }
                    error.toString() == InvalidClient.toString() -> {
                        Toast.makeText(this, "유효하지 않은 앱", Toast.LENGTH_SHORT).show()
                    }
                    error.toString() == InvalidGrant.toString() -> {
                        Toast.makeText(this, "인증 수단이 유효하지 않아 인증할 수 없는 상태", Toast.LENGTH_SHORT)
                            .show()
                    }
                    error.toString() == InvalidRequest.toString() -> {
                        Toast.makeText(this, "요청 파라미터 오류", Toast.LENGTH_SHORT).show()
                    }
                    error.toString() == InvalidScope.toString() -> {
                        Toast.makeText(this, "유효하지 않은 scope ID", Toast.LENGTH_SHORT).show()
                    }
                    error.toString() == Misconfigured.toString() -> {
                        Toast.makeText(
                            this,
                            "설정이 올바르지 않음(android key hash)",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                    error.toString() == ServerError.toString() -> {
                        Toast.makeText(this, "서버 내부 에러", Toast.LENGTH_SHORT).show()
                    }
                    error.toString() == Unauthorized.toString() -> {
                        Toast.makeText(this, "앱이 요청 권한이 없음", Toast.LENGTH_SHORT).show()
                    }
                    else -> { // Unknown
                        Log.e(TAG, "로그인 실패", error)
                        Log.d(TAG, "onCreate: ${error}")
                        Toast.makeText(this, "기타 에러", Toast.LENGTH_SHORT).show()
                    }
                }
            } else if (token != null) {
                Log.d(TAG, "token ${token} error ${error}")
                Log.i(TAG, "로그인 성공 ${token.accessToken}")
                Toast.makeText(this, "로그인에 성공하였습니다.", Toast.LENGTH_SHORT).show()

                //로그인 정보 서버에 등록
                //서버에 고객정보 저장
                registerMenberToServer()

//***********************
//                val intent = Intent(this, SelectP2pOrServerActivity::class.java)
//                startActivity(intent)

                if(roomAddress.isNullOrEmpty()){
                    val intent = Intent(this, SelectP2pOrServerActivity::class.java)
                    startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
                }
                else{
                    val intent = Intent(this, ServerPhotoRoomActivity::class.java)
                    intent.putExtra("roomAddress",roomAddress )
                    startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
                }
            }
        }

        kakao_login_button.setOnClickListener {
            Log.d(TAG, "onCreate: kakao_login_button")
            if (UserApiClient.instance.isKakaoTalkLoginAvailable(this)) {
                UserApiClient.instance.loginWithKakaoTalk(this, callback = callback)
            } else {
                UserApiClient.instance.loginWithKakaoAccount(this, callback = callback)
            }
        }

    }

    fun registerMenberToServer() {

        mSocket = SocketUtill.createAndConnetSocket()!!

        UserApiClient.instance.me { user, error ->
            if (error != null) {
                Log.e(TAG, "사용자 정보 요청 실패", error)
            } else if (user != null) {
                var scopes = mutableListOf<String>()
                if (user.kakaoAccount?.emailNeedsAgreement == true) {
                    scopes.add("account_email")
                }
                if (user.kakaoAccount?.birthdayNeedsAgreement == true) {
                    scopes.add("birthday")
                }
                if (user.kakaoAccount?.birthyearNeedsAgreement == true) {
                    scopes.add("birthyear")
                }
                if (user.kakaoAccount?.genderNeedsAgreement == true) {
                    scopes.add("gender")
                }
                if (user.kakaoAccount?.phoneNumberNeedsAgreement == true) {
                    scopes.add("phone_number")
                }
                if (user.kakaoAccount?.profileNeedsAgreement == true) {
                    scopes.add("profile")
                }
                if (user.kakaoAccount?.ageRangeNeedsAgreement == true) {
                    scopes.add("age_range")
                }
                if (user.kakaoAccount?.ciNeedsAgreement == true) {
                    scopes.add("account_ci")
                }

                if (scopes.count() > 0) {
                    Log.d(TAG, "사용자에게 추가 동의를 받아야 합니다.")

                    UserApiClient.instance.loginWithNewScopes(this, scopes) { token, error ->
                        if (error != null) {
                            Log.e(TAG, "사용자 추가 동의 실패", error)
                        } else {
                            Log.d(TAG, "allowed scopes: ${token!!.scopes}")

                            // 사용자 정보 재요청
                            UserApiClient.instance.me { user, error ->
                                if (error != null) {
                                    Log.e(TAG, "사용자 정보 요청 실패", error)
                                } else if (user != null) {
                                    Log.i(TAG, "사용자 정보 요청 성공")
                                }
                            }
                        }
                    }
                }

                //send to server id, nickname, profile url
                val firebasetoken = FirebaseInstanceId.getInstance().token
                mSocket.emit(
                    "RegisterMemberToDB",
                    user.id,
                    user.kakaoAccount?.profile?.nickname,
                    user.kakaoAccount?.profile?.profileImageUrl,
                    firebasetoken
                )
                Log.i(
                    TAG, "사용자 정보 요청 성공" +
                            "\n회원번호: ${user.id}" +
                            "\n닉네임: ${user.kakaoAccount?.profile?.nickname}" +
                            "\n프로필사진: ${user.kakaoAccount?.profile?.thumbnailImageUrl}"
                )
                mSocket.close()
            }
        }
    }

    // 권한 요청 부분(우리는 갤러리를 위한 WRITE / READ, WiFi - D를 위한 LOCATION, INTERNET이 필요함) -> 권한 부분도 구멍이 많아서 처리해줘야함!!!
    private fun requestPermissionToUser() {
        var writePermission =
            ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
        var readPermission =
            ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
        var locationPermission =
            ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
        var recordAudioPermission =
            ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)

        if (writePermission == PackageManager.PERMISSION_DENIED
            || readPermission == PackageManager.PERMISSION_DENIED
            || locationPermission == PackageManager.PERMISSION_DENIED
            || recordAudioPermission == PackageManager.PERMISSION_DENIED
        ) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(
                    Manifest.permission.WRITE_EXTERNAL_STORAGE,
                    Manifest.permission.READ_EXTERNAL_STORAGE,
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.RECORD_AUDIO
                ),
                1
            )
        }
    }

    @RequiresApi(Build.VERSION_CODES.P)
    fun getHash() {
        try {
            val info =
                packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNING_CERTIFICATES)
            val signatures = info.signingInfo.apkContentsSigners
            val md = MessageDigest.getInstance("SHA")
            for (signature in signatures) {
                val md: MessageDigest
                md = MessageDigest.getInstance("SHA")
                md.update(signature.toByteArray())
                val key = String(Base64.encode(md.digest(), 0))
                Log.d("Hash Key: ", "!@!@!$key!@!@!")
            }
        } catch (e: Exception) {
            Log.e("not fount", e.toString())
        }
    }

}