package com.example.pic_pho.WaitingRoomServer

import android.app.Activity
import android.app.Dialog
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import android.view.Gravity
import android.view.View
import android.widget.TextView
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.exifinterface.media.ExifInterface
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.pic_pho.App
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.createAndConnectSocket
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.mSocket
import com.example.pic_pho.ImageHandler.ImageHandler
import com.example.pic_pho.ImageHandler.ImageHandler.Companion.compressImage
import com.example.pic_pho.LoginActivity
import com.example.pic_pho.MakeGroup.MakeGroupActivity
import com.example.pic_pho.PhotoRoomServer.FileUtil
import com.example.pic_pho.PhotoRoomServer.FriendsPhotoCountModel
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity.Companion.photoPickedList
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity.Companion.photoPickedUriList
import com.example.pic_pho.PhotoRoomServer.ServerThumbnailPhotoModel
import com.example.pic_pho.R
import com.example.pic_pho.databinding.ActivityWaitingRoomServerBinding
import com.github.nkzawa.emitter.Emitter
import com.github.nkzawa.socketio.client.Ack
import com.google.gson.Gson
import com.google.gson.JsonObject
import com.kakao.sdk.user.UserApiClient
import com.snatik.storage.Storage
import id.zelory.compressor.loadBitmap
import kotlinx.android.synthetic.main.activity_waiting_room_server.*
import kotlinx.android.synthetic.main.item_waiting_room_server.*
import kotlinx.coroutines.*
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import org.json.JSONArray
import java.io.File

class ServerWaitingRoomActivity : AppCompatActivity(), ServerWaitingRoomInterface {

    data class GroupMember(
        val UserID: String,
        val NickName: String,
        val ProfileUrl: String,
        val IsHost: Boolean,
        var status: Int
    )


    private lateinit var binding: ActivityWaitingRoomServerBinding
    private val TAG = "서버대기방"

    private lateinit var serverWaitingRoomAdapter: ServerWaitingRoomAdapter

    var infoOfUser: JsonObject? = null
    var numOfMyPhoto: Int = 0
    private var actualImage: File? = null
    lateinit var exif: ExifInterface
    private var compressedImage: File? = null
    var roomAddr: String? = null
    var roomName: String? = null
    private var dialog: Dialog? = null

    var returnedImage: Bitmap? = null

    // 총 내가 받은 사진 개수
    var numOfReceivedPhoto: Int = 0

    // 친구들이 사진을 다 보냈는지 확인하는 어레이 리스트
    var friendsCount: Int = 0
    var receivedFriendsCount: Int = 0
    var friendsPhotoCountList: MutableMap<String, FriendsPhotoCountModel> = mutableMapOf()


    var userTempImage: String? = null

    companion object {
        var photoModelList = ArrayList<ServerThumbnailPhotoModel>()
        var myKakaoId: String? = null
        var userKakaoNickName: String? = null

        // 서버에서 삭제를 위한 storage 정의
        var serverStorage: Storage? = null
        var serverFilePathList = ArrayList<String>()
        var serverWaitingRoomActivity: Activity? = null

        var invitedFriendsList = ArrayList<GroupMember>()
        var forScanFilePathList = ArrayList<String>()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWaitingRoomServerBinding.inflate(layoutInflater)
        setContentView(binding.root)
        serverWaitingRoomActivity = this
        runBlocking {
            try {
                photoModelList.clear()
                photoPickedUriList?.clear()
                photoPickedList?.clear()
                invitedFriendsList?.clear()
            } catch (e: IndexOutOfBoundsException) {
                Log.d(TAG, ":온바인드뷰홀더케치")
            }
        }



        Log.d(TAG, "onCreate: 서버 웨이팅 룸")
        dialog?.dismiss()

        if (mSocket == null)
            mSocket = createAndConnectSocket()



        LoginActivity.requestPermissionToUser(this)

        runBlocking {
            CoroutineScope(Dispatchers.IO).launch {
                //note 4. 모든 사람들이 들어온 경우 사진을 선택할수있게 한다.
                mSocket!!.on("DoSelectPhoto", DoSelectPhoto)
                //note 7. 서버는 클라이언트가 보내는 사진을 전송
                mSocket!!.on("SendPictureFromServer", imageReturn)
                mSocket!!.on("enterMember", showEnteredMember)
                mSocket!!.on("startPhotoRoom", startPhotoRoom)
                mSocket!!.on("selectStatus", skipFriend)
                delay(100)
            }.join()
        }

        serverWaitingRoomAdapter = ServerWaitingRoomAdapter(invitedFriendsList)
        binding.waitingMemberRecyclerview.apply {
            layoutManager = LinearLayoutManager(
                this@ServerWaitingRoomActivity,
                LinearLayoutManager.VERTICAL,
                false
            )
            adapter = serverWaitingRoomAdapter
        }

        UserApiClient.instance.me { user, error ->
            if (error != null) {
                Log.e(TAG, "사용자 정보 요청 실패", error)
            } else if (user != null) {
                userKakaoNickName = user.kakaoAccount?.profile?.nickname.toString()
                userTempImage = user.kakaoAccount?.profile?.profileImageUrl.toString()
                Log.d(
                    TAG, "user.kakaoAccount?.profile?.nickname.toString()" +
                            "${user.kakaoAccount?.profile?.nickname.toString()}" +
                            "${user.kakaoAccount?.profile?.profileImageUrl.toString()}" +
                            "onActivityResult: pictureowner"
                )
            }
        }

        // 삭제를 위한 storage init
        serverStorage = Storage(applicationContext)

        //note 대기방으로 넘어오는 경우
        //note 1. 주소획득
        Log.d(TAG, "gogogogogogogo: ")
        roomAddr = intent.getStringExtra("roomAddress")
        roomName = intent.getStringExtra("roomName")
        var ishost = intent.getBooleanExtra("isHost", false)
        var jsonobjectlist = intent.getSerializableExtra("invitedFriendsJsonArray")

        // note 1-1. 만약 호스트라면 강제시작, 다시 초대 버튼 활성화 시켜주기
        if (ishost) {
            binding.buttonReinvite.visibility = View.VISIBLE
            binding.buttonForceStart.visibility = View.VISIBLE
        }


        Log.d(TAG, "invitedFriendsJsonArray: ${jsonobjectlist}, roomAddress is $roomAddr")
        //note 2. 서버에 접속
        //mSocket = SocketUtil.createAndConnectSocket()
//        mSocket = SocketUtil.getSocket()
//        mSocket!!.on("enterMember", showEnteredMember)
//        //note 4. 모든 사람들이 들어온 경우 사진을 선택할수있게 한다.
//        mSocket!!.on("DoSelectPhoto", DoSelectPhoto)
//        //note 7. 서버는 클라이언트가 보내는 사진을 전송
//        mSocket!!.on("SendPictureFromServer", imageReturn)
//
//        mSocket!!.connect()

//
//        runBlocking {
//            CoroutineScope(Dispatchers.IO).launch {
//                //note 리스너는 앞쪽에 배치
//                //note 3.2 들어오는 사람들을 리사이클러뷰에 표시한다.

//            }.join()
//        }


        Log.d(TAG, "onCreate: ${roomAddr}")
        Log.d(TAG, "ishost: ${ishost}")
        if (roomAddr != null) {
            //note 3. 서버에 접속 성공하면, 클라이언트는 서버로 자신의 정보를 보내고, 서버는 접속 정보를 모든 방에 접속한 사람들에게 보냄
            if (mSocket != null) {
                //note 3.1 보내야 하는 정보는 userId = model.userId, name = model.name, profileImage = model.profileImage
                UserApiClient.instance.me { user, error ->
                    if (error != null) {
                        Log.e(TAG, "사용자 정보 요청 실패", error)
                        infoOfUser = null
                    } else if (user != null) {
                        Log.d(TAG, "enterToWaitingroomWithInvitation")
                        infoOfUser = JsonObject()
                        infoOfUser!!.addProperty("UserID", user.id.toString())
                        myKakaoId = user.id.toString()
                        infoOfUser!!.addProperty(
                            "NickName",
                            user.kakaoAccount?.profile?.nickname.toString()
                        )
                        infoOfUser!!.addProperty(
                            "ProfileImg",
                            user.kakaoAccount?.profile?.profileImageUrl.toString()
                        )
                        Log.d(TAG, "getUserInfo11: ${infoOfUser}")
                        if (ishost) {
                            infoOfUser!!.addProperty("IsHost", "True")
                            infoOfUser!!.addProperty("roomName", roomName)
                            Log.d(
                                TAG,
                                "onCreate: before emit host room Addr $roomAddr, infoOfUser $infoOfUser, size is ${MakeGroupActivity.invitedFriendsJsonArray.size()}"
                            )
                            mSocket!!.emit(
                                "enterRoom",
                                roomAddr,
                                infoOfUser,
                                MakeGroupActivity.invitedFriendsJsonArray.size()
                            )
                        } else {
                            infoOfUser!!.addProperty("IsHost", "False")
                            Log.d(
                                TAG,
                                "onCreate: before emit client room Addr $roomAddr, infoOfUser is $infoOfUser"
                            )
                            mSocket!!.emit("enterRoom", roomAddr, infoOfUser, 0)
                        }
                    }
                }
            }
        }


        //note 8. 클라이언트는 서버로 부터 받는 진행상황을 모두 실시간으로 업데이트

        //note 9. 모든 사진이 받아지면 포토룸으로 이동


        //note 리사이클러 뷰에 대한 내용
        //note 사진 선택 클릭되면 선택 시 정보를 서버로 보냄.
        binding.serverChoosePhotoCardview.setOnClickListener {
            Log.d(
                TAG,
                "onCreate: ACTION_GET_CONTENTACTION_GET_CONTENTACTION_GET_CONTENTACTION_GET_CONTENTACTION_GET_CONTENTACTION_GET_CONTENT"
            )
            var intent = ImageHandler.selectPhoto()
//            var intent = Intent(Intent.ACTION_GET_CONTENT)
            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
            intent.data = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
            intent.type = "image/*"
            intent.addFlags(
                Intent.FLAG_GRANT_READ_URI_PERMISSION
                        or Intent.FLAG_GRANT_WRITE_URI_PERMISSION
                        or Intent.FLAG_GRANT_PERSISTABLE_URI_PERMISSION
                        or Intent.FLAG_GRANT_PREFIX_URI_PERMISSION
            )
            intent.addCategory(Intent.CATEGORY_OPENABLE)

            var userid: String? = null

            UserApiClient.instance.me { user, error ->
                if (error != null) {
                    userid = null
                } else if (user != null) {
                    userid = user.id.toString()
                }

            }
            Log.d(TAG, "onCreate: ${userid}")
            mSocket!!.emit("selectStatus", 1, roomAddr, infoOfUser)
            //serverWaitingRoomAdapter.modelList[0].status = 1

            startActivityForResult(intent, 100)
        }
    }

    var skipFriend = Emitter.Listener {
        var skipFriendKakaoId: String = it[0].toString()
        friendsPhotoCountList[skipFriendKakaoId]!!.isDone = true
        receivedFriendsCount++
        Log.d(TAG, "스킵 프렌드 들어왔을 때: 스킵 프렌드 들어왔을 때")
        // 다 받았는지 확인하는 로직
        if (friendsCount == receivedFriendsCount) {
            //note sort
            runBlocking {
                CoroutineScope(Dispatchers.Default).launch {
                    var sortedModelList =
                        photoModelList.sortedWith(
                            compareBy(
                                { it.taketime },
                                { it.pictureowner })
                        )
                    photoModelList.clear()
                    photoModelList.addAll(sortedModelList)
                    delay(100)

                    Log.d(TAG, "정렬skipFriend 끝났을 때 photoModelList size : ${photoModelList.size}")
                }.join()
                Log.d(TAG, "정렬skipFriend 끝~~~: 정렬 끝~~~~")
            }
            // 사진 싹 다 받았으면 한번 정렬해주기!
            mSocket!!.emit("receivedAll", myKakaoId, roomAddr)
        }
    }


    override fun onResume() {
        if (mSocket == null)
            mSocket = createAndConnectSocket()
        super.onResume()
        Log.d(TAG, "onResume: 서버 웨이팅 룸")
    }

    override fun onItemClicked() {
        TODO("Not yet implemented")
    }

    override fun onDestroy() {
        dialog?.dismiss()
        super.onDestroy()
        Log.d(TAG, "onDestroy: 서버 웨이팅 룸")
    }

    override fun onBackPressed() {
//        super.onBackPressed()
//        mSocket!!.disconnect()

        runBlocking {
            CoroutineScope(Dispatchers.Main).launch {
                dialog =
                    ServerPhotoRoomActivity.showDialog(
                        context = this@ServerWaitingRoomActivity,
                        resource = R.layout.dialog_leave_waitingroom,
                        gravity = Gravity.CENTER,
                        color = Color.WHITE
                    )
                dialog!!.findViewById<TextView>(R.id.button_leave).setOnClickListener {
                    dialog?.dismiss()
                    mSocket!!.emit("leaveRoom", Ack {
                        Log.e(TAG, "onBackPressed: leaveRoom ${it[0]}")
                        if (it[0].equals("received")) {
                            Log.e(TAG, "onBackPressed: leaveRoom 진입!!!!!!!!!")
                            finish()
                        }
                    })
                }

                dialog!!.findViewById<TextView>(R.id.button_continue).setOnClickListener {
                    dialog?.dismiss()
                }
            }
        }
    }

    var startPhotoRoom = Emitter.Listener {
        CoroutineScope(Dispatchers.IO).launch {
            mSocket!!.off("enterMember")
            mSocket!!.off("SendPictureFromServer")
            mSocket!!.off("startPhotoRoom")
            mSocket!!.off("selectStatus")
            delay(100)
        }
        Log.d(
            TAG,
            "startPhotoRoom:startPhotoRoomstartPhotoRoomstartPhotoRoomstartPhotoRoomstartPhotoRoom "
        )
        val intent = Intent(App.instance, ServerPhotoRoomActivity::class.java)
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        intent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
        intent.putExtra("roomAddress", roomAddr)
        startActivity(intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP))
    }


    //note 5.1 사진 선택을 완료하면 선택완료 정보를 서버로 보냄,
    //note 5.2 서버는 모든 송신 여부 정보를 방의 모든 클라이언트에게 송신
    var showEnteredMember = Emitter.Listener {
        Log.d(TAG, "showEnteredMember: showEnteredMember")
        Log.d(TAG, "it[0]: ${it[0]}")
        try {
            Log.d(TAG, "트라이 들어왔다 ㅋㅋ: ")
            runBlocking {
                invitedFriendsList.clear()
            }
            var jsonArray: JSONArray = JSONArray(it[0].toString())
            var gson = Gson()
            friendsCount = jsonArray.length() - 1
            for (i in 0 until jsonArray.length()) {
                var jsonstring = jsonArray.get(i).toString()
                var member = gson.fromJson(jsonstring, GroupMember::class.java)

                Log.d(TAG, "member.UserID: ${member.UserID},myKakaoId is $myKakaoId")

                if (member.UserID != myKakaoId && !friendsPhotoCountList.containsKey(member.UserID)) {
                    Log.d(TAG, "이프문안: ")
                    friendsPhotoCountList[member.UserID] = FriendsPhotoCountModel()
                }
                invitedFriendsList.add(member)
            }
            Log.d(TAG, "쇼 엔터 멤버 끝날때 invited friends list 에는? : $invitedFriendsList")
            serverWaitingRoomNotifyDatasetChanged()

        } catch (e: IndexOutOfBoundsException) {
            Log.d(TAG, "캐치 들어왔다 ㄸ: ")
        }
    }

    fun serverWaitingRoomNotifyDatasetChanged() {
        CoroutineScope(Dispatchers.Main).launch(Dispatchers.Main) {
            if (serverWaitingRoomAdapter != null) {
                try {
                    delay(100)
                    serverWaitingRoomAdapter?.notifyDataSetChanged()
                } catch (e: IndexOutOfBoundsException) {
                    Log.d(TAG, "serverWaitingRoomNotifyDatasetChanged: 노티 익셉션")
                }

            } else
                Log.d(TAG, "serverWaitingRoomNotifyDatasetChanged: 서버 웨이팅 룸 어댑터는 널이었다.")
        }
    }


    var DoSelectPhoto = Emitter.Listener {
        Log.d(TAG, "DoSelectPhoto: DoSelectPhoto")
        CoroutineScope(Dispatchers.Main).launch {
            binding.serverChoosePhotoCardview.visibility = View.VISIBLE
            binding.hostButtons.visibility = View.INVISIBLE
        }
        mSocket!!.off("DoSelectPhoto")
    }

    //note 6. 사진을 모든 클라이언트가 사진을 선택한 경우 사진을 서버로 보냄
    @RequiresApi(Build.VERSION_CODES.Q)
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when (requestCode) {
            100 -> {
                var userName: String = userKakaoNickName!!
                var userImage: String = userTempImage!!
                var pictureowner: String = myKakaoId!!

                UserApiClient.instance.me { user, error ->
                    if (error != null) {
                        Log.e(TAG, "사용자 정보 요청 실패", error)
                    } else if (user != null) {
                        userName = user.kakaoAccount?.profile?.nickname.toString()
                        userImage = user.kakaoAccount?.profile?.profileImageUrl.toString()
                        Log.d(
                            TAG, "user.kakaoAccount?.profile?.nickname.toString()" +
                                    "${user.kakaoAccount?.profile?.nickname.toString()}" +
                                    "${user.kakaoAccount?.profile?.profileImageUrl.toString()}" +
                                    "onActivityResult: pictureowner $pictureowner"
                        )
                    }
                }
                if (data != null) {
                    if (data.clipData != null) {
                        val count = data.clipData!!.itemCount
                        //내가 가져온 사진 개수 저장
                        numOfMyPhoto = count
                        for (i in 0 until count) {
                            var imageUri = data.clipData!!.getItemAt(i).uri
                            var taketime: String? = null

                            var absolutePath: String =
                                ImageHandler.getFullPathFromUri(this, imageUri)!!

                            val takeFlags: Int = intent.flags and
                                    (Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                            contentResolver.takePersistableUriPermission(imageUri, takeFlags)

                            serverFilePathList.add(
                                absolutePath
                            )
                            actualImage = FileUtil.from(App.instance, imageUri)


                            //메타정보추출하기
                            exif = ExifInterface(actualImage!!)
                            if (exif != null) {
                                taketime = exif.getAttribute(ExifInterface.TAG_DATETIME).toString()
                                Log.d(TAG, "onActivit사진 선택했을때yResult: taketime $taketime")
                                if (taketime == null)
                                    taketime = System.currentTimeMillis().toString()
                            }
                            //압축하기
                            runBlocking {
                                compressedImage =
                                    compressImage(actualImage!!, this@ServerWaitingRoomActivity)
                            }



                            CoroutineScope(Dispatchers.IO).launch {
//                        //압축한 파일 보내기
                                var image_string =
                                    ImageHandler.bitmapToString(loadBitmap(compressedImage!!))
                                mSocket!!.emit(
                                    "SendPictureFromClient",
                                    image_string,
                                    roomAddr,
                                    taketime,
                                    pictureowner,
                                    i,
                                    count,
                                    userName,
                                    userImage
                                )

                                //modelList에 넣어두기
                                var photoinfo = ServerThumbnailPhotoModel(
                                    imageUri,
                                    taketime,
                                    pictureowner,
                                    i,
                                    count,
                                    userName,
                                    userImage,
                                    absolutePath = absolutePath
                                )

                                photoModelList.add(photoinfo)
                            }

                        }
                    } else { // 사진을 한장만 선택했을 경우
                        val imageUri = data.data
                        var taketime: String? = null
                        var absolutePath: String = ImageHandler.getFullPathFromUri(this, imageUri)!!
                        // 절대경로 추가
                        serverFilePathList.add(
                            absolutePath
                        )

                        val takeFlags: Int = intent.flags and
                                (Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION)
                        contentResolver.takePersistableUriPermission(imageUri!!, takeFlags)

                        actualImage = FileUtil.from(App.instance, imageUri)

                        exif = ExifInterface(actualImage!!)
                        if (exif != null) {
                            taketime = exif.getAttribute(ExifInterface.TAG_DATETIME).toString()
                        }

                        //압축하기
                        runBlocking {
                            compressedImage =
                                compressImage(actualImage!!, this@ServerWaitingRoomActivity)
                        }


                        CoroutineScope(Dispatchers.IO).launch {
//                        //압축한 파일 보내기
                            var image_string =
                                ImageHandler.bitmapToString(loadBitmap(compressedImage!!))
                            mSocket!!.emit(
                                "SendPictureFromClient",
                                image_string,
                                roomAddr,
                                taketime,
                                pictureowner,
                                0,
                                1,
                                userName,
                                userImage
                            )

                            var photoinfo = ServerThumbnailPhotoModel(
                                imageUri,
                                taketime,
                                pictureowner,
                                0,
                                1,
                                username = userName,
                                userimg = userImage,
                                absolutePath = absolutePath
                            )
                            Log.d(TAG, "onActivityResult: username $userName, userimg $userImage")

                            photoModelList.add(photoinfo)
                        }
                    }
                    mSocket!!.emit("selectStatus", 2, roomAddr, infoOfUser)
                } else//사진을 한장도 안보냈을 때
                    mSocket!!.emit("selectStatus", 3, roomAddr, infoOfUser)

                binding.serverChoosePhotoCardview.visibility = View.GONE
            }
        }
    }


    val mutex = Mutex()


    // 사진을 서버로부터 받는 곳!
    var imageReturn = Emitter.Listener { it ->

        Log.d(TAG, "사진을 서버로부터 받는 곳!: 사진을 서버로부터 받는 곳!")
        var data = it[0].toString()
        var receivedtaketime = it[1].toString()
        var receivedowner = it[2].toString()
        // 전체중에 몇장 오고있는지
        var currentorder = it[3].toString()
        // 그 사람이 보내야하는 전체 사진수
        var totalcount = it[4].toString().toInt()
        // 그룹전체가 보내는 전체 사진수
        var sum_totalCount = it[5].toString()
        // 네명다 사진을 보내기 시작했는지??
        var is_everyone = it[6].toString().toInt()
        var username = it[7].toString()
        var userimg = it[8].toString()
        Log.d(TAG, "username: $username,, userimg $userimg")

        Log.d(TAG, "receivedowner: $receivedowner and myKakaoId is $myKakaoId")

//        friendsPhotoCountList[receivedowner]!!.goalPhotoCounts = totalcount
//        (friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts)++

        returnedImage = ImageHandler.convertString64ToImage(data)
        runBlocking {
            CoroutineScope(Dispatchers.Default).launch {
                Log.d(
                    TAG,
                    "friendsPhotoCountList[receivedowner]!!.received전전전PhotoCounts: ${friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts}"
                )
                mutex.withLock {
                    friendsPhotoCountList[receivedowner]!!.goalPhotoCounts = totalcount
                    (friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts)++
                }
                Log.d(
                    TAG,
                    "friendsPhotoCountList[receivedowner]!!.receivedP후후후hotoCounts: ${friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts}"
                )
                Log.d(
                    TAG,
                    "friendsPhotoCountList: ${friendsPhotoCountList}, size is ${friendsPhotoCountList.size}"
                )


                var filepath: String = "/sdcard" + "/DCIM/Picpho/"
                var filename: String =
                    "Picpho_" + System.currentTimeMillis().toString() + ".jpg"
//                "Picpho_" + receivedowner + "_" + System.currentTimeMillis().toString() + ".jpg"
                var fullFilePath: String = filepath + filename
                // 절대 경로 저장
                serverFilePathList.add(fullFilePath)
                // 스캔용 파일 패스 리스트에도 저장
                forScanFilePathList.add(fullFilePath)

                var file = File(fullFilePath)
                // 디렉토리 존재하지 않으면 디렉토리 생성
                val dirs = File(file.parent.toString())
                if (!dirs.exists()) dirs.mkdirs()
                ImageHandler.saveBitmapAsFile(
                    returnedImage!!,
                    file,
                    receivedtaketime,
                    receivedowner
                )
                //modelList에 넣어두기43
//            var photoinfo = ServerThumbnailPhotoModel(Uri.fromFile(file!!))
                var photoinfo = ServerThumbnailPhotoModel(
                    Uri.fromFile(file),
                    receivedtaketime,
                    receivedowner,
                    currentorder.toInt(),
                    totalcount.toInt(),
                    absolutePath = fullFilePath,
                    username = username,
                    userimg = userimg
                )
                photoModelList.add(photoinfo)
                numOfReceivedPhoto++

                Log.e(
                    "받은 사진",
                    "${numOfReceivedPhoto} vs ${sum_totalCount.toInt() - numOfMyPhoto}"
                )
                Log.d(
                    TAG, "friendsPhotoCountList[receivedowner]!!.goalPhotoCounts: " +
                            "${friendsPhotoCountList[receivedowner]!!.goalPhotoCounts}" +
                            "friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts" +
                            "${friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts}"
                )

                if (friendsPhotoCountList[receivedowner]!!.goalPhotoCounts
                    == friendsPhotoCountList[receivedowner]!!.receivedPhotoCounts
                ) {
                    Log.d(TAG, "is Done true 할때!!!: is Done true 할때!!!")
                    friendsPhotoCountList[receivedowner]!!.isDone = true
                    receivedFriendsCount++
                }

                Log.d(
                    TAG,
                    "다 받았는지 확인하는 로직: friendsCount $friendsCount receivedFriendsCount $receivedFriendsCount"
                )

                // 다 받았는지 확인하는 로직
                if (friendsCount == receivedFriendsCount) {
                    //note sort
                    var sortedModelList =
                        photoModelList.sortedWith(
                            compareBy(
                                { it.pictureowner },
                                { it.taketime }
                            )
                        )
                    photoModelList.clear()
                    photoModelList.addAll(sortedModelList)

                    Log.d(TAG, "정렬 끝났을 때 photoModelList size : ${photoModelList.size}")
                    Log.d(TAG, "정렬 끝~~~: 정렬 끝~~~~")
                    // 사진 싹 다 받았으면 한번 정렬해주기!
                    mSocket!!.emit("receivedAll", myKakaoId, roomAddr)
                }
                Log.d(
                    TAG,
                    "go to photoroom: ${numOfReceivedPhoto} || ${sum_totalCount.toInt()} || ${numOfMyPhoto}"
                )


            }


            //FIREBASE ALARM 파이어베이스 알람 다시 보내기
            fun reInviteFriends(view: View) {
                Log.d(TAG, "ServerWaitingRoomActivity - reInviteFriends() called")


                var jsonObjectList = intent.getSerializableExtra("invitedFriendsJsonArray")
                Log.e(TAG, "제이슨 오브젝트 리스트: ${jsonObjectList}")

                roomName = intent.getStringExtra("roomName").toString()
                Log.e(TAG, "룸 네임: ${roomName}")

                mSocket!!.emit(
                    "selectedGroup",
                    MakeGroupActivity.invitedFriendsJsonArray, roomAddr, roomName
                )
            }

            //친구들 다 안들어왔을 때도 강제로 시작하기
            fun forcedStart(view: View) {
                mSocket!!.emit("forcedStart", roomAddr)
            }

        }
    }
}
