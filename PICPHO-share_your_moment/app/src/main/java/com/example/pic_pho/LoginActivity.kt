package com.example.pic_pho

import android.Manifest
import android.app.Activity
import android.app.Dialog
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.util.Base64
import android.util.Log
import android.view.Gravity
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.createAndConnectSocket
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.mSocket
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.WaitingRoomServer.ServerWaitingRoomActivity
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity
import com.example.pic_pho.databinding.ActivityLoginBinding
import com.google.firebase.iid.FirebaseInstanceId
import com.kakao.sdk.auth.model.OAuthToken
import com.kakao.sdk.common.model.AuthErrorCause.*
import com.kakao.sdk.user.UserApiClient
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.security.MessageDigest

class LoginActivity : AppCompatActivity() {
    private val TAG = "LoginActivity"

    //친구 초대 받았을 때
    lateinit var intentfromfirebase: Intent // = getIntent()


    val callBack: (OAuthToken?, Throwable?) -> Unit = { token, error ->
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
            registerMemberToServer()

//***********************
//                val intent = Intent(this, SelectP2pOrServerActivity::class.java)
//                startActivity(intent)

//            if (roomAddress.isNullOrEmpty()) {/**/
            mSocket?.disconnect()
            mSocket = null

            val intent = Intent(this, SelectP2pOrServerActivity::class.java)
            startActivity(intent)
//            } else {
//                val intent = Intent(this, ServerWaitingRoomActivity::class.java)
//                intent.putExtra("roomAddress", roomAddress)
//                intent.putExtra("test", "1")
//                startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
//            }
        }
    }

    companion object {
        var roomAddress: String? = null


        fun requestPermissionToUser(activity: Activity) {
            var writePermission =
                ContextCompat.checkSelfPermission(
                    App.instance,
                    Manifest.permission.WRITE_EXTERNAL_STORAGE
                )
            var readPermission =
                ContextCompat.checkSelfPermission(
                    App.instance,
                    Manifest.permission.READ_EXTERNAL_STORAGE
                )
            var locationPermission =
                ContextCompat.checkSelfPermission(
                    App.instance,
                    Manifest.permission.ACCESS_FINE_LOCATION
                )
            var recordAudioPermission =
                ContextCompat.checkSelfPermission(App.instance, Manifest.permission.RECORD_AUDIO)

            if (writePermission == PackageManager.PERMISSION_DENIED
                || readPermission == PackageManager.PERMISSION_DENIED
                || locationPermission == PackageManager.PERMISSION_DENIED
                || recordAudioPermission == PackageManager.PERMISSION_DENIED
            ) {
                ActivityCompat.requestPermissions(
                    activity,
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

        var loginActivity : Activity? = null


    }

    private lateinit var binding: ActivityLoginBinding
    private var dialogLogin: Dialog? = null


    @RequiresApi(Build.VERSION_CODES.P)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)
        loginActivity = this

        if (dialogLogin != null)
            dialogLogin!!.dismiss()




        UserApiClient.instance.accessTokenInfo { tokenInfo, error ->
            if (error != null) {
                Toast.makeText(this, "토큰 정보 보기 실패", Toast.LENGTH_SHORT).show()
            } else if (tokenInfo != null) {
                Toast.makeText(this, "토큰 정보 보기 성공", Toast.LENGTH_SHORT).show()

//                runBlocking {
//                    CoroutineScope(Dispatchers.IO).launch {
                registerMemberToServer()
//                    }.join()
//                }

                if (roomAddress.isNullOrEmpty()) {

                    val intent = Intent(this, SelectP2pOrServerActivity::class.java)
                    startActivity(intent)
                    finish()
                } else {
//                    val intent = Intent(this, ServerWaitingRoomActivity::class.java)
//                    intent.putExtra("roomAddress", roomAddress)
//                    intent.putExtra("test", "3")
//                    startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
                }
            }
        }

        //일단 초대 받은거면 방 번호를 받아둔다.
        roomAddress = null
        intentfromfirebase = getIntent()
        if (intentfromfirebase != null) {
            roomAddress = intentfromfirebase.extras?.getString("roomAddress")
            Toast.makeText(this, "${roomAddress}", Toast.LENGTH_SHORT).show()

            //note 초대를 받아서 로그인창으로 넘어오는 경우.
            if (roomAddress != null) {
                UserApiClient.instance.accessTokenInfo { tokenInfo, error ->
                    if (error != null) {
                        Toast.makeText(this, "초대 받았으나 로그인 되어있지 않음.", Toast.LENGTH_SHORT).show()
                    } else if (tokenInfo != null) {
                        var waitingroomIntent: Intent =
                            Intent(this, ServerWaitingRoomActivity::class.java)
                        waitingroomIntent.putExtra("roomAddress", roomAddress)
                        waitingroomIntent.putExtra("test", "2")
                        startActivity(waitingroomIntent)
                        finish()
                    }
                }

            }
        }

        requestPermissionToUser(this) //todo : Wifi 사용 중인지 점검하는 퍼미션 체크 필요


//        getHash() //디버깅용 해시 얻는 함수


        binding.kakaoLoginButton.setOnClickListener {
            Log.d(TAG, "onCreate: kakao_login_button")
            if (UserApiClient.instance.isKakaoTalkLoginAvailable(this)) {
                UserApiClient.instance.loginWithKakaoTalk(this, callback = callBack)
            } else {
                UserApiClient.instance.loginWithKakaoAccount(this, callback = callBack)
            }
        }
    }

    override fun onResume() {
        super.onResume()
        val networkStatus : Boolean = NetworkStatus.isConnected(this)
        if (!networkStatus){
            runBlocking {
                CoroutineScope(Dispatchers.Main).launch {
                    dialogLogin =
                        ServerPhotoRoomActivity.showDialog(
                            context = loginActivity!!,
                            resource = R.layout.dialog_invite,
                            gravity = Gravity.BOTTOM,
                            color = Color.WHITE
                        )

                    dialogLogin!!.findViewById<TextView>(R.id.cancelText).setOnClickListener {
                        Log.d(TAG, "showDoYouWantClaimDialog: 다이얼로그 취소 눌림")
                        dialogLogin!!.dismiss()
                    }
                    dialogLogin!!.findViewById<TextView>(R.id.switchToP2pText).setOnClickListener {
                        Log.d(TAG, "showDoYouWantClaimDialog: 다이얼로그 취소 눌림")
                        switchToWifiRoom()
                        dialogLogin!!.dismiss()
                    }
                }
            }
        }
    }

    override fun onDestroy() {
        if (dialogLogin != null)
            dialogLogin!!.dismiss()
        super.onDestroy()
    }

    fun switchToWifiRoom(){
        val intent = Intent(this, WifiDirectMainActivity::class.java)
        startActivity(intent)
    }



    fun registerMemberToServer() {

        Log.d(TAG, "registerMemberToServer: start")
        UserApiClient.instance.me { user, error ->
            if (error != null) {
                Log.e(TAG, "사용자 정보 요청 실패", error)
            } else if (user != null) {
                mSocket = createAndConnectSocket()

                //send to server id, nickname, profile url
                val firebasetoken = FirebaseInstanceId.getInstance().token

                runBlocking {
                    CoroutineScope(Dispatchers.IO).launch {
                        mSocket!!.emit(
                            "RegisterMemberToDB",
                            user.id,
                            user.kakaoAccount?.profile?.nickname,
                            user.kakaoAccount?.profile?.profileImageUrl,
                            firebasetoken)
                    }.join()
                }

                Log.i(
                    TAG, "사용자 정보 요청 성공" +
                            "\n회원번호: ${user.id}" +
                            "\n닉네임: ${user.kakaoAccount?.profile?.nickname}" +
                            "\n프로필사진: ${user.kakaoAccount?.profile?.thumbnailImageUrl}"
                )
            }
        }

    }


    // 권한 요청 부분(우리는 갤러리를 위한 WRITE / READ, WiFi - D를 위한 LOCATION, INTERNET이 필요함) -> 권한 부분도 구멍이 많아서 처리해줘야함!!!


    @RequiresApi(Build.VERSION_CODES.P)
    fun getHash() {
        try {
            val info =
                packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNING_CERTIFICATES)
            val signatures = info.signingInfo.apkContentsSigners
            for (signature in signatures) {
                val messageDigest: MessageDigest = MessageDigest.getInstance("SHA")
                messageDigest.update(signature.toByteArray())
                val key = String(Base64.encode(messageDigest.digest(), 0))
                Log.d("Hash Key: ", "!@!@!$key!@!@!")
            }
        } catch (e: Exception) {
            Log.e("not fount", e.toString())
        }
    }

}