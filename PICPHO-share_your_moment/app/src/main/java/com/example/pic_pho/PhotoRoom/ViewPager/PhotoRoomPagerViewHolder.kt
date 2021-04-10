package com.example.pic_pho.PhotoRoom.ViewPager

import android.content.Intent
import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.PhotoRoom.PhotoRoomActivity.Companion.drawerPhotoUriList
import com.example.pic_pho.PhotoRoom.PhotoRoomActivity.Companion.drawerRecyclerAdapter
import com.example.pic_pho.PhotoRoom.ThumbnailPhotoModel
import com.example.pic_pho.PhotoRoomServer.ServerPhotoEnlargeActivity
import com.example.pic_pho.R
import com.example.pic_pho.WifiDirect.UI.WifiDrawer.DrawerPhotoModel
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity.Companion.filePathList
import kotlinx.android.synthetic.main.item_photoroom_pager.view.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class PhotoRoomPagerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val itemImage = itemView.SelectedPhoto
    private val bookMarkImage = itemView.imageView_bookmark_wifi
    private var drawerPhotoModel: DrawerPhotoModel? = null
    private val maxImage = itemView.imageView_photomax_wifi

    fun bindWithView(thumbnailPhotoModel: ThumbnailPhotoModel) {
        CoroutineScope(Dispatchers.Main).launch {
            Glide
                .with(App.instance)
                .load(thumbnailPhotoModel.thumbnailPhoto)
                .into(itemImage)

            if (thumbnailPhotoModel.isPicked) {
                bookMarkImage.setImageResource(R.drawable.bookmark_fill)
            } else {
                bookMarkImage.setImageResource(R.drawable.bookmark_2)
            }
        }



        bookMarkImage.setOnClickListener {
            if (thumbnailPhotoModel.isPicked) {
                CoroutineScope(Dispatchers.Main).launch {
                    bookMarkImage.setImageResource(R.drawable.bookmark_2)
                }
                thumbnailPhotoModel.isPicked = false
                drawerPhotoUriList.remove(thumbnailPhotoModel.thumbnailPhoto!!)
                // 사진 삭제
                filePathList.add(thumbnailPhotoModel.path!!)
            } else {
                CoroutineScope(Dispatchers.Main).launch {
                    bookMarkImage.setImageResource(R.drawable.bookmark_fill)
                }
                thumbnailPhotoModel.isPicked = true
                drawerPhotoUriList.add(thumbnailPhotoModel.thumbnailPhoto!!)
                // 사진 삭제를 위한 추가
                filePathList.remove(thumbnailPhotoModel.path!!)
                Log.d("사진이 삭제되는 이유에 관하여", "bindWithView: ${thumbnailPhotoModel.path!!}")
            }
            drawerRecyclerAdapter.notifyDataSetChanged()

        }

        maxImage.setOnClickListener {
            var intent = Intent(App.instance, ServerPhotoEnlargeActivity::class.java)
            intent.putExtra("uri", thumbnailPhotoModel.thumbnailPhoto.toString())
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            App.instance.startActivity(intent)
        }

    }
}