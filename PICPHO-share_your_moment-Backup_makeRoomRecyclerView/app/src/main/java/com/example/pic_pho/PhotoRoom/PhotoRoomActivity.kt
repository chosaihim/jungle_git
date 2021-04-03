package com.example.pic_pho.PhotoRoom

import android.content.ClipData
import android.net.Uri
import android.os.Bundle
import android.util.DisplayMetrics
import android.util.Log
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.viewpager2.widget.ViewPager2
import com.example.pic_pho.App
import com.example.pic_pho.PhotoRoom.ViewPager.PhotoRoomPagerAdapter
import com.example.pic_pho.R
import com.example.pic_pho.WifiDirect.WifiDirectBroadcastReceiver
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity
import com.example.pic_pho.databinding.ActivityPhotoroomBinding
import com.example.pic_pho.databinding.ItemPhotoroomPagerBinding
import java.io.File

class PhotoRoomActivity : AppCompatActivity(), ThumbnailRecyclerViewInterface {

    val TAG: String = "로그"
    var photoModelList = ArrayList<ThumbnailPhotoModel>()

    companion object {
        lateinit var thumbnailRecyclerAdapter: ThumbnailRecyclerAdapter
        lateinit var photoRoomPagerAdapter : PhotoRoomPagerAdapter
        lateinit var binding: ActivityPhotoroomBinding
        lateinit var photobinding: ItemPhotoroomPagerBinding

        fun changeSelectedPhotoByClicked(position : Int){
            binding.photoroomViewPager.setCurrentItem(position)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityPhotoroomBinding.inflate(layoutInflater)
        setContentView(binding.root)
    }

    override fun onResume() {
        super.onResume()
        photobinding = ItemPhotoroomPagerBinding.inflate(layoutInflater)

        if(!WifiDirectMainActivity.photoInfoList.isEmpty()) {
            var uri : Uri

            for (photo in WifiDirectMainActivity.photoInfoList) {
                Log.d(TAG, "onResume: 포토룸에서 URI Item에 바인딩 : ${photo.photoUri}")

                if(photo.photoOwnerIP.equals("picpho")){
                    uri = photo.photoUri
                }else {
                    uri = Uri.fromFile(File(photo.photoUri.toString()))
                    photo.photoUri = uri // Uri 가공해서, Photo List 업데이트
                }
                var photoModel = ThumbnailPhotoModel(thumbnailPhoto = uri)
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
        binding.PhotoRoomRecyclerView.apply {
            layoutManager = LinearLayoutManager(
                this@PhotoRoomActivity,
                LinearLayoutManager.HORIZONTAL,
                false
            )
            adapter = thumbnailRecyclerAdapter
        }

        var photoOldPosition : Int = 0
        val displayMetrics = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(displayMetrics)

        var width = displayMetrics.widthPixels / 3


        binding.photoroomViewPager.registerOnPageChangeCallback(object : ViewPager2.OnPageChangeCallback(){
            override fun onPageSelected(position: Int) {
                super.onPageSelected(position)
                var photoNewPosition : Int = 0
                val photoLastIndex : Int = thumbnailRecyclerAdapter.itemCount - 1
                // 원래 보고 있던 포지션과 바뀐 포지션을 비교해서 중앙으로 보내주는 부분
                if (photoOldPosition > position) {
                    photoNewPosition = position -1
                } else if ( photoOldPosition < position) {
                    photoNewPosition = position + 1
                }

                // 바뀐 포지션이 index 마지막이었다면
                if (position == photoLastIndex){
                    photoNewPosition = photoLastIndex
//                    val param = btnClickMe.layoutParams as ViewGroup.MarginLayoutParams
//                    param.setMargins(10,10,10,10)
//                    btnClickMe.layoutParams = param // Tested!! - You need this line for the params to be applied.
                    val param = binding.PhotoRoomRecyclerView.layoutParams as ViewGroup.MarginLayoutParams
                    param.setMargins(0,0,width,0)
                    binding.PhotoRoomRecyclerView.layoutParams = param
                }
                // 바뀐 포지션이 index 처음이라면
                else if (position == 0){
                    photoNewPosition = 0
                    val param = binding.PhotoRoomRecyclerView.layoutParams as ViewGroup.MarginLayoutParams
                    param.setMargins(width,0,0,0)
                    binding.PhotoRoomRecyclerView.layoutParams = param
                }
                else{
                    val param = binding.PhotoRoomRecyclerView.layoutParams as ViewGroup.MarginLayoutParams
                    param.setMargins(0,0,0,0)
                    binding.PhotoRoomRecyclerView.layoutParams = param
                }
                binding.PhotoRoomRecyclerView.smoothScrollToPosition(photoNewPosition)
//                binding.PhotoRoomRecyclerView.scrollToPosition(photoNewPosition)
                photoOldPosition = position
            }
        })
    }

    override fun onBackPressed() {
        super.onBackPressed()
        WifiDirectMainActivity.removeGroup()
        if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
            WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
        }
    }

    override fun onStop() {
        super.onStop()
        Log.d(TAG, "onStop: onStop on PhotoRoomActivity")

        // Server Thread가 계속 Loop 되는 것을 방지하기 위함. Thread.cancel 활용
        if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
            WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
        }
        WifiDirectMainActivity.removeGroup()
    }

    override fun onDestroy() {
        super.onDestroy()
        Log.d("onDestroy", "onDestroy")

        // Server Thread가 계속 Loop 되는 것을 방지하기 위함. Thread.cancel 활용
        if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
            WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
        }
        WifiDirectMainActivity.removeGroup()
    }

    //function for finish action
    fun finishAction(view: View) {
        Log.d(TAG, "PhotoRoomActivity - () called")
        Toast.makeText(
            App.instance,
            "끝내기!!!!!",
            Toast.LENGTH_SHORT
        ).show()
        finish()
    }

//    private fun changeDP(value : Int) : Int{
//        var displayMetrics = resources.displayMetrics
//        return (value * displayMetrics.density).roundToInt()
//    }
}