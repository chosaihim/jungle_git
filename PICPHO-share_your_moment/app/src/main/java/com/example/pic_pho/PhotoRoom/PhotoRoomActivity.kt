package com.example.pic_pho.PhotoRoom

import android.app.Activity
import android.app.Dialog
import android.content.Intent
import android.graphics.Color
import android.media.MediaScannerConnection
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.Gravity
import android.view.View
import android.view.animation.Animation
import android.view.animation.AnimationUtils
import android.widget.LinearLayout
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.viewpager2.widget.ViewPager2
import com.example.pic_pho.PhotoRoom.ViewPager.PhotoRoomPagerAdapter
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.R
import com.example.pic_pho.UnCatchTaskService
import com.example.pic_pho.WifiDirect.FileReceiveActionThread
import com.example.pic_pho.WifiDirect.UI.HorizontalItemDecoration
import com.example.pic_pho.WifiDirect.UI.VerticalItemDecoration
import com.example.pic_pho.WifiDirect.UI.WifiDrawer.DrawerPhotoModel
import com.example.pic_pho.WifiDirect.UI.WifiDrawer.DrawerRecyclerAdapter
import com.example.pic_pho.WifiDirect.WaitingForOwnerActivity.Companion.waitingForOwnerActivity
import com.example.pic_pho.WifiDirect.WifiDirectBroadcastReceiver
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity.Companion.filePathList
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity.Companion.isGroupOwner
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity.Companion.photoInfoList
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity.Companion.storage
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity.Companion.wifiDirectMainActivity
import com.example.pic_pho.databinding.ActivityPhotoroomBinding
import com.example.pic_pho.databinding.ItemPhotoroomPagerBinding
import kotlinx.coroutines.*
import java.io.File

class PhotoRoomActivity : AppCompatActivity(), ThumbnailRecyclerViewInterface {

    val TAG: String = "로그"
    var photoModelList = ArrayList<ThumbnailPhotoModel>()
    var drawerPhotoList = PhotoRoomActivity.drawerPhotoList
    private var drawer: LinearLayout? = null
    private var drawerCover: LinearLayout? = null
    private var isPageOpen = false
    private var dialog: Dialog? = null

    companion object {
        lateinit var thumbnailRecyclerAdapter: ThumbnailRecyclerAdapter
        lateinit var photoRoomPagerAdapter: PhotoRoomPagerAdapter
        lateinit var drawerRecyclerAdapter: DrawerRecyclerAdapter
        lateinit var binding: ActivityPhotoroomBinding
        lateinit var photobinding: ItemPhotoroomPagerBinding
        var drawerPhotoList = ArrayList<DrawerPhotoModel>()
        var drawerPhotoUriList = ArrayList<Uri>()
        fun changeSelectedPhotoByClicked(position: Int) {
            CoroutineScope(Dispatchers.Main).launch {
                binding.photoroomViewPager.currentItem = position
            }
        }

        var scanFileForOwnerList = ArrayList<File>()
        var photoRoomActivity: Activity? = null
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)


        binding = ActivityPhotoroomBinding.inflate(layoutInflater)
        setContentView(binding.root)

        photobinding = ItemPhotoroomPagerBinding.inflate(layoutInflater)

        startService(Intent(this, UnCatchTaskService::class.java))

        if (!photoInfoList.isEmpty()) {
            var uri: Uri
            for (photo in photoInfoList) {
                Log.d(TAG, "onResume: 포토룸에서 URI Item에 바인딩 : ${photo.photoUri}")

                if (photo.photoOwnerIP.equals("picpho")) {
                    uri = photo.photoUri!!
                } else {
                    uri = Uri.fromFile(File(photo.photoUri.toString()))
                    photo.photoUri = uri // Uri 가공해서, Photo List 업데이트
                }
                var photoModel =
                    ThumbnailPhotoModel(thumbnailPhoto = uri, path = photo.absolutePath)
                var drawerPhotoModel = DrawerPhotoModel(drawerPhotoUri = uri)
                this.photoModelList.add(photoModel)
            }
        }

        // 인스턴스 생성
        thumbnailRecyclerAdapter = ThumbnailRecyclerAdapter(this)
        thumbnailRecyclerAdapter.submitList(this.photoModelList)
        photoRoomPagerAdapter = PhotoRoomPagerAdapter(this.photoModelList)

        binding.photoroomViewPager.apply {
            adapter = photoRoomPagerAdapter
            orientation = ViewPager2.ORIENTATION_HORIZONTAL
        }
        //레이아웃 매니저
        //여기서 4F는 리사이클러뷰 이동속도를 이야기함. 자신의 원하는 속도를 위해선
        // 4F, 2F , 8F 등으로 속도 조절이 가능하다.
//        var linearLayoutManager : VariableScrollSpeedLinearLayoutManager =
//            VariableScrollSpeedLinearLayoutManager(this, 2F)
//        linearLayoutManager.orientation = LinearLayoutManager.HORIZONTAL
        binding.PhotoRoomRecyclerView.apply {
            layoutManager = LinearLayoutManager(
                this@PhotoRoomActivity,
                LinearLayoutManager.HORIZONTAL,
                false
            )
            adapter = thumbnailRecyclerAdapter
            addItemDecoration(HorizontalItemDecoration(10))
        }
        CoroutineScope(Dispatchers.Main).launch {
            delay(100)
            thumbnailRecyclerAdapter.notifyDataSetChanged()
        }
        drawerRecyclerAdapter = DrawerRecyclerAdapter(drawerPhotoUriList)


        binding.photoroomDrawalPhotosRecyclerview.apply {
            layoutManager = GridLayoutManager(
                this@PhotoRoomActivity,
                3,
                LinearLayoutManager.VERTICAL,
                false
            )
            adapter = drawerRecyclerAdapter
            CoroutineScope(Dispatchers.Main).launch {
                addItemDecoration(HorizontalItemDecoration(10))
                addItemDecoration(VerticalItemDecoration(20))
            }
        }


        var photoOldPosition: Int = 0



        binding.photoroomViewPager.registerOnPageChangeCallback(object :
            ViewPager2.OnPageChangeCallback() {
            override fun onPageSelected(position: Int) {
                super.onPageSelected(position)
                var photoNewPosition: Int = 0
                val photoLastIndex: Int = thumbnailRecyclerAdapter.itemCount - 1
                // 원래 보고 있던 포지션과 바뀐 포지션을 비교해서 중앙으로 보내주는 부분
                if (photoOldPosition > position) {
                    photoNewPosition = position - 1
                } else if (photoOldPosition < position) {
                    photoNewPosition = position + 1
                }
                CoroutineScope(Dispatchers.Main).launch {
                    // 바뀐 포지션이 index 마지막이었다면
                    if (position == photoLastIndex)
                        photoNewPosition = photoLastIndex

                    // 바뀐 포지션이 index 처음이라면
                    else if (position == 0)
                        photoNewPosition = 0

                    binding.PhotoRoomRecyclerView.smoothScrollToPosition(photoNewPosition)
                    photoOldPosition = position
                }
                CoroutineScope(Dispatchers.Main).launch {
                    delay(100)
                    photoRoomPagerAdapter.notifyDataSetChanged()
                }
            }
        })

        photoRoomActivity = this

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
            CoroutineScope(Dispatchers.Main).launch {
                clickDrawer(leftAnimation, rightAnimation)
            }
        }

        binding.imageViewPhotoRoomExit.setOnClickListener {
            showDoYouWantLeaveThisRoom()
        }

        binding.textViewExitphotoRoomExit.setOnClickListener {
            showDoYouWantLeaveThisRoom()
        }

        binding.textviewLeavePhotoRoom.setOnClickListener {
            showDoYouWantLeaveThisRoom()
        }






        if (isGroupOwner) {
            val fileCount: Int = scanFileForOwnerList.size
            Log.d(
                TAG,
                "onCreate: WifiDirectMainActivity.filePathList.size ${scanFileForOwnerList.size}"
            )
            for (i in 0 until fileCount)
                FileReceiveActionThread.scanFile(this, scanFileForOwnerList[i], "jpg")
        }
    }

    fun clickDrawer(leftAnimation: Animation, rightAnimation: Animation) {
        CoroutineScope(Dispatchers.Main).launch {
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
    }

    override fun onResume() {
        super.onResume()

    }

    fun beforeFinish() {
        CoroutineScope(Dispatchers.IO).launch {
            WifiDirectMainActivity.removeGroup()
            if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
                WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
            }
        }
    }

    override fun onBackPressed() {
        if (binding.drawerPhotoRoom.visibility == View.VISIBLE) {
            binding.drawerCover.visibility = View.GONE
            binding.drawerPhotoRoom.visibility = View.GONE
        } else
            showDoYouWantLeaveThisRoom()
    }

    override fun onStop() {
        beforeFinish()
        super.onStop()
        Log.d(TAG, "onStop: onStop on PhotoRoomActivity")
        // Server Thread가 계속 Loop 되는 것을 방지하기 위함. Thread.cancel 활용
    }

    override fun onDestroy() {
        beforeFinish()
        super.onDestroy()
        Log.d("onDestroy", "onDestroy")
        // Server Thread가 계속 Loop 되는 것을 방지하기 위함. Thread.cancel 활용
    }

    fun showDoYouWantLeaveThisRoom() {
        runBlocking {
            CoroutineScope(Dispatchers.Main).launch {
                dialog =
                    ServerPhotoRoomActivity.showDialog(
                        context = photoRoomActivity!!,
                        resource = R.layout.dialog_leave_photoroom,
                        gravity = Gravity.BOTTOM,
                        color = Color.WHITE
                    )

                dialog!!.findViewById<TextView>(R.id.button_leave).setOnClickListener {
                    Log.d(TAG, "showDoYouWantClaimDialog: 다이얼로그 취소 눌림")
                    finishAction()
                    dialog!!.dismiss()
                }
                dialog!!.findViewById<TextView>(R.id.button_continue).setOnClickListener {
                    Log.d(TAG, "showDoYouWantClaimDialog: 다이얼로그 취소 눌림")
                    dialog!!.dismiss()
                }
            }
        }
    }

    //function for finish action
    fun finishAction() {
        Log.d(TAG, "PhotoRoomActivity - () called")
        beforeFinish()
        runBlocking {
            CoroutineScope(Dispatchers.Default).launch {
                val deletePhotoSize: Int = filePathList.size
                Log.d(TAG, "finishAction: 파일패스리스트에는 $filePathList")
                for (i in 0 until deletePhotoSize) {
                    storage!!.deleteFile(filePathList[i])
                    scanFileByPath(filePathList[i], "jpg")
                }
            }.join()
        }
        wifiDirectMainActivity?.finish()
        waitingForOwnerActivity?.finish()
        finish()
    }

    fun scanFileByPath(absolutePath: String, mimeType: String) {
        Log.d(TAG, "scanFileByPath: 시작 absolutePath is $absolutePath")
        runBlocking {
            CoroutineScope(Dispatchers.Default).launch {
                MediaScannerConnection
                    .scanFile(
                        applicationContext,
                        arrayOf(absolutePath),
                        arrayOf(mimeType),
                        null
                    )
            }.join()
        }
        Log.d(TAG, "scanFileByPath: 종료 absolutePath is $absolutePath")
    }
}