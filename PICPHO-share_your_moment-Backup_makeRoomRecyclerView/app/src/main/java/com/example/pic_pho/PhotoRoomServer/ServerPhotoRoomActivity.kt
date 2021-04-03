package com.example.pic_pho.PhotoRoomServer

import android.R.attr.button
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.media.AudioManager
import android.media.MediaScannerConnection
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.provider.Settings
import android.util.Base64
import android.util.Log
import android.view.View
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.widget.LinearLayout
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import androidx.exifinterface.media.ExifInterface
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.viewpager2.widget.ViewPager2
import com.example.pic_pho.App
import com.example.pic_pho.CellularSocket.SocketUtill
import com.example.pic_pho.GroupVoiceCall.AGEventHandler
import com.example.pic_pho.GroupVoiceCall.EngineEventHandler
import com.example.pic_pho.GroupVoiceCall.WorkerThread
import com.example.pic_pho.Lobby.LobbyActivity
import com.example.pic_pho.PhotoRoomServer.ViewPager.ServerPhotoRoomPagerAdapter
import com.example.pic_pho.R
import com.example.pic_pho.databinding.ActivityServerphotoroomBinding
import com.example.pic_pho.databinding.ItemPhotoroomPagerBinding
import com.github.nkzawa.emitter.Emitter
import com.github.nkzawa.socketio.client.IO
import com.github.nkzawa.socketio.client.Socket
import id.zelory.compressor.Compressor
import id.zelory.compressor.constraint.format
import id.zelory.compressor.constraint.quality
import id.zelory.compressor.loadBitmap
import kotlinx.android.synthetic.main.activity_photoroom.*
import kotlinx.android.synthetic.main.activity_photoroom.PhotoRoomRecyclerView
import kotlinx.android.synthetic.main.activity_photoroom.photoroom_view_pager
import kotlinx.android.synthetic.main.activity_serverphotoroom.*
import kotlinx.android.synthetic.main.item_photoroom_pager.*
import kotlinx.coroutines.*
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream
import java.net.URISyntaxException
import kotlin.concurrent.thread


class ServerPhotoRoomActivity : AppCompatActivity(), ServerThumbnailRecyclerViewInterface,
    AGEventHandler {

    val TAG: String = "로그"
    var returnedImage: Bitmap? = null
    lateinit var mSocket: Socket;
    lateinit var exif: ExifInterface
    private var actualImage: File? = null
    private var compressedImage: File? = null
    private var photoFlag = false
    private var drawer : LinearLayout? = null
    private var drawerCover : LinearLayout? = null
    private var isPageOpen = false
    private var engineEventHandler: EngineEventHandler? = null
    private val photoModelList = ArrayList<ServerThumbnailPhotoModel>()

    @Volatile
    private var mAudioRouting = -1

    @Volatile
    private var mAudioMuted = false

    var numOfRecievedPhoto: Int = 0
    var numOfExpectedPhoto: Int = 0
    var numOfMyPhoto: Int = 0
    var workerThread: WorkerThread? = null
    var roomAddress: String? =null
    var numOfMembers:Int=0

    companion object {
        lateinit var serverThumbnailRecyclerAdapter: ServerThumbnailRecyclerAdapter
        lateinit var serverPhotoRoomPagerAdapter: ServerPhotoRoomPagerAdapter
        lateinit var binding: ActivityServerphotoroomBinding
        lateinit var photobinding: ItemPhotoroomPagerBinding

        fun changeSelectedPhotoByClicked(position: Int) {
            binding.photoroomViewPager.setCurrentItem(position)
        }

        fun scanFile(context: Context?, f: File, mimeType: String) {
            MediaScannerConnection
                .scanFile(context, arrayOf(f.absolutePath), arrayOf(mimeType), null)
        }

        fun getExif(file: File) {
            var exif = ExifInterface(file!!)
            if (exif != null) {
                var myAttribute: String? = "[Exif information] \n\n"
                myAttribute += "TAG_DATETIME           ::: " + exif.getAttribute(ExifInterface.TAG_DATETIME)
                    .toString() + "\n"
                myAttribute += "TAG_ARTIST             ::: " + exif.getAttribute(ExifInterface.TAG_ARTIST)
                    .toString() + "\n"
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "onCreate: ")
        binding = ActivityServerphotoroomBinding.inflate(layoutInflater)
        setContentView(binding.root)


//        val intent: Intent = getIntent()


        // socket 통신 시작\
        mSocket = SocketUtill.createAndConnetSocket()!!


        //방이름을 먼저 찾아봅니다!

        mSocket.on("SendPictureFromServer", imageReturn)
        mSocket.on("done", imageRecieveDone)
        mSocket.on("privateRoomSuccess", privateRoomSuccess)

        photoFlag = false

        //사진 내려받을 때 쓰는 변수들 초기화
        numOfExpectedPhoto = 0
        numOfMyPhoto = 0

        // Group Call 시작
        val intent = intent
        val channel = intent.getStringExtra("roomAddress")

//        val channel = "picpho"
        App.initWorkerThread()
        workerThread = App.workerThread
        engineEventHandler = workerThread!!.eventHandler()
        engineEventHandler!!.addEventHandler(this)
        workerThread!!.joinChannel(channel, workerThread!!.engineConfig.mUid)
        volumeControlStream = AudioManager.STREAM_VOICE_CALL

        // Animation 시작
        drawer = binding.drawerPhotoRoom
        drawerCover = binding.drawerCover
        val leftAnimation = AnimationUtils.loadAnimation(this, R.anim.translate_left)
        val rightAnimation = AnimationUtils.loadAnimation(this, R.anim.translate_right)

        binding.imageViewPhotoRoomMoreAction.setOnClickListener {
            CoroutineScope(Dispatchers.Main).launch {
                clickDrawer(leftAnimation, rightAnimation)
            }
        }
        binding.drawerEmpty.setOnClickListener {
            clickDrawer(leftAnimation, rightAnimation)
        }
    }

    fun clickDrawer(leftAnimation: Animation, rightAnimation: Animation){
        if (isPageOpen) {
            Log.d("TAG", "true")
            drawerCover!!.visibility = View.GONE
            drawer!!.startAnimation(rightAnimation)
            drawer!!.visibility = View.GONE
            isPageOpen = false
        } else {
            Log.d("TAG", "false")
            drawerCover!!.visibility = View.VISIBLE
            drawer!!.visibility = View.VISIBLE
            drawer!!.startAnimation(leftAnimation)
            isPageOpen = true
        }
    }

    fun recyclerviewSortByID() {
        var sortedModelList = photoModelList.sortedBy { it.taketime }
        sortedModelList = sortedModelList.sortedBy { it.pictureowner }
        photoModelList.clear()
        photoModelList.addAll(sortedModelList)

        runOnUiThread {
            serverThumbnailRecyclerAdapter.notifyDataSetChanged()
            serverPhotoRoomPagerAdapter.notifyDataSetChanged()
        }
    }


    override fun onStart() {
        super.onStart()
        Log.d(TAG, "onStart: ")
        roomAddress = intent.getStringExtra("roomAddress")
        numOfMembers = intent.getIntExtra("numOfMembers",0)
        Toast.makeText(this, "${roomAddress}", Toast.LENGTH_SHORT).show()
        mSocket.emit("privateRoom", roomAddress.toString(), numOfMembers)


        if(!photoFlag) {
            var intent = Intent(Intent.ACTION_PICK)
            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
            intent.data = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
            intent.type = "image/*"
            startActivityForResult(intent, 100)
            photoFlag = true
        }
    }

    override fun onResume() {
        super.onResume()
        photobinding = ItemPhotoroomPagerBinding.inflate(layoutInflater)

        // 인스턴스 생성
        serverThumbnailRecyclerAdapter = ServerThumbnailRecyclerAdapter(this)
        serverThumbnailRecyclerAdapter.submitList(this.photoModelList)
        serverPhotoRoomPagerAdapter = ServerPhotoRoomPagerAdapter(this.photoModelList)
        binding.photoroomViewPager.apply {
            adapter = serverPhotoRoomPagerAdapter
            orientation = ViewPager2.ORIENTATION_HORIZONTAL
        }
        PhotoRoomRecyclerView.apply {
            layoutManager = LinearLayoutManager(
                this@ServerPhotoRoomActivity,
                LinearLayoutManager.HORIZONTAL,
                false
            )
            adapter = serverThumbnailRecyclerAdapter
        }
    }


    override fun onStop() {
        super.onStop()
        Log.d(TAG, "onStop: ")
        Log.d(TAG, "onStop: onStop on PhotoRoomActivity")

    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("onDestroy", "onDestroy")
        if (workerThread != null) {
            workerThread!!.leaveChannel(workerThread!!.engineConfig.mChannel)
        }
        if (engineEventHandler != null) {
            engineEventHandler!!.removeEventHandler(this)
        }
        quitPhotoRoom()
        mSocket.disconnect()
    }

    // GroupCall 관련 함수
    private fun quitPhotoRoom() {
        val intent = Intent(this, LobbyActivity::class.java)
        startActivity(intent)
        finish()
    }

    fun onVoiceMuteClicked(view: View) {
        Log.d(TAG, "onVoiceMuteClicked: $view audio_status: $mAudioMuted")
        workerThread!!.rtcEngine!!.muteLocalAudioStream(!mAudioMuted.also { mAudioMuted = it })
        mAudioMuted = !mAudioMuted
    }

    override fun onJoinChannelSuccess(channel: String, uid: Int, elapsed: Int) {
        Log.d(TAG, "onJoinChannelSuccess: ${channel}")
        runOnUiThread(Runnable {
            if (isFinishing) {
                return@Runnable
            }
            Log.d(TAG, "onJoinChannelSuccess: ${mAudioMuted}")
            workerThread!!.rtcEngine!!.muteLocalAudioStream(mAudioMuted)
        })
    }

    override fun onUserOffline(uid: Int, reason: Int) {
        Log.d(TAG, "onUserOffline: " + (uid and 0xFFFFFFFFL.toInt()) + " " + reason)
    }

    override fun onExtraCallback(type: Int, vararg data: Any?) {
        runOnUiThread(Runnable {
            if (isFinishing) {
                return@Runnable
            }
            doHandleExtraCallback(type, *data as Array<out Any>)
        })
    }

    private fun doHandleExtraCallback(type: Int, vararg data: Any) {
    }

    @RequiresApi(Build.VERSION_CODES.Q)
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when (requestCode) {
            100 -> {
                if (data != null) {
                    val count = data?.clipData!!.itemCount

                    //내가 가져온 사진 개수 저장
                    numOfMyPhoto = count

                    for (i in 0 until count) {
                        var imageUri = data.clipData!!.getItemAt(i).uri
                        var taketime: String? = null
                        var pictureowner: String? = null

                        //압축
                        //원본 파일 가져오기
                        actualImage = FileUtil.from(this, imageUri)

                        //메타정보추출하기
                        exif = ExifInterface(actualImage!!)
                        if (exif != null) {
                            taketime = exif.getAttribute(ExifInterface.TAG_DATETIME).toString()
//                            pictureowner = exif.getAttribute(ExifInterface.TAG_ARTIST).toString()
                            var ANDROID_ID: String = Settings.Secure.getString(
                                applicationContext.contentResolver,
                                Settings.Secure.ANDROID_ID
                            )
                            pictureowner = ANDROID_ID
                        }
                        //압축하기
                        runBlocking {
                            compressedImage = compressImage(actualImage!!)
                        }

                        //modelList에 넣어두기
                        var photoinfo = ServerThumbnailPhotoModel(
                            imageUri,
                            taketime!!,
                            pictureowner!!,
                            i,
                            count
                        )
                        photoModelList.add(photoinfo)

                        //압축한 파일 보내기
                        var image_string = BitmapToString(loadBitmap(compressedImage!!))
                        mSocket.emit("SendPictureFromClient", image_string , roomAddress, taketime, pictureowner, i, count)
                    }
                }
            }
        }
    }

    var privateRoomSuccess = Emitter.Listener {
//        Toast.makeText(this, "${it[0].toString()}", Toast.LENGTH_SHORT).show()
        Log.d("서버", "it[0].toString(): ${it[0].toString()}")
    }

    //서버에서 사진 받았을 때 실행되는 함수
    var imageReturn = Emitter.Listener {
        var data = it[0].toString()
        var receivedtaketime = it[1].toString()
        var receivedowner = it[2].toString()
        var currentorder = it[3].toString()
        var tocalcount = it[4].toString()
        var sum_totalCount = it[5].toString()
        var is_everyone = it[6].toString().toInt()

        returnedImage = convertString64ToImage(data)

        thread() {
            var filepath: String = "/sdcard" + "/DCIM/Picpho_test/"
            var filename: String =
                "Picpho_" + System.currentTimeMillis().toString() + ".jpg"
//                "Picpho_" + receivedowner + "_" + System.currentTimeMillis().toString() + ".jpg"
            var file = File(filepath + filename)
            // 디렉토리 존재하지 않으면 디렉토리 생성
            val dirs = File(file!!.parent.toString())
            if (!dirs.exists()) dirs.mkdirs()
            saveBitmapAsFile(returnedImage!!, file, receivedtaketime, receivedowner)
            scanFile(this, file!!, "jpg")


            //modelList에 넣어두기
//            var photoinfo = ServerThumbnailPhotoModel(Uri.fromFile(file!!))
            var photoinfo = ServerThumbnailPhotoModel(
                Uri.fromFile(file!!),
                receivedtaketime,
                receivedowner,
                currentorder.toInt(),
                tocalcount.toInt()
            )
            photoModelList.add(photoinfo)
            numOfRecievedPhoto++

            Log.e("받은 사진", "${numOfRecievedPhoto} vs ${sum_totalCount.toInt() - numOfMyPhoto}")
            // 사진 싹 다 받았으면 한번 정렬해주기!
            if (numOfRecievedPhoto == sum_totalCount.toInt() - numOfMyPhoto) // && is_everyone == 1)
            {
                recyclerviewSortByID()
            }
        }
    }

    var imageRecieveDone = Emitter.Listener {
        numOfExpectedPhoto = it[0].toString().toInt() - numOfMyPhoto

        runOnUiThread() {
            Toast.makeText(
                App.instance,
                "개 이미지 보내기 완료!!!",
                Toast.LENGTH_SHORT
            ).show()
        }

    }

    suspend fun compressImage(originalImage: File): File? {
        var ResultImage: File? = null
        coroutineScope {
            launch {
                // Default compression
                ResultImage = Compressor.compress(this@ServerPhotoRoomActivity, originalImage!!)
                {
//                    resolution(1500, 1500)
                    quality(95)
                    format(Bitmap.CompressFormat.JPEG)
//                    size(1_097_152) // 2 MB
                }
            }
        }
        return ResultImage
    }

    fun convertString64ToImage(base64String: String): Bitmap {
        val decodedString = Base64.decode(base64String, Base64.DEFAULT)
        return BitmapFactory.decodeByteArray(decodedString, 0, decodedString.size)
    }

    fun BitmapToString(bitmap: Bitmap): String? {
        val baos = ByteArrayOutputStream() //바이트 배열을 차례대로 읽어 들이기위한 ByteArrayOutputStream클래스 선언
        bitmap.compress(Bitmap.CompressFormat.JPEG, 90, baos) //bitmap을 압축 (숫자 70은 70%로 압축한다는 뜻)
        val bytes: ByteArray = baos.toByteArray() //해당 bitmap을 byte배열로 바꿔준다.
        return Base64.encodeToString(bytes, Base64.DEFAULT) //String을 retrurn
    }

    fun saveBitmapAsFile(
        bitmap: Bitmap,
        file: File,
        receivedtaketime: String,
        receivedowner: String
    ) {
        var os: OutputStream? = null
        try {
            file.createNewFile()
            os = FileOutputStream(file)
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, os)
            exif = ExifInterface(file!!)
            exif.setAttribute(ExifInterface.TAG_DATETIME, receivedtaketime)
            exif.setAttribute(ExifInterface.TAG_ARTIST, receivedowner)
            exif.saveAttributes()
            getExif(file!!)
            os.close()
        } catch (e: java.lang.Exception) {
            e.printStackTrace()
        }
    }

    fun saveBitmapAsFile(bitmap: Bitmap, file: File) {
        var os: OutputStream? = null
        try {
            file.createNewFile()
            os = FileOutputStream(file)
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, os)
            os.close()
        } catch (e: java.lang.Exception) {
            e.printStackTrace()
        }
    }
}