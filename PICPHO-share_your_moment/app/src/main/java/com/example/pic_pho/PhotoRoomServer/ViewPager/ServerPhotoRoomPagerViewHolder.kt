package com.example.pic_pho.PhotoRoomServer.ViewPager

import android.content.Intent
import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.mSocket
import com.example.pic_pho.ImageHandler.ImageHandler.Companion.getOrientationOfImage
import com.example.pic_pho.PhotoRoomServer.ServerPhotoEnlargeActivity
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity.Companion.photoPickedList
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity.Companion.photoPickedUriList
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity.Companion.serverDrawerPickAdapter
import com.example.pic_pho.PhotoRoomServer.ServerThumbnailPhotoModel
import com.example.pic_pho.R
import com.example.pic_pho.WaitingRoomServer.ServerWaitingRoomActivity.Companion.serverFilePathList
import kotlinx.android.synthetic.main.item_photoroom_pager.view.SelectedPhoto
import kotlinx.android.synthetic.main.item_serverphotoroom_pager.view.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class ServerPhotoRoomPagerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val itemImage = itemView.SelectedPhoto
    private val favoriteImage = itemView.imageView_favorite_server
    private val bookmarkImage = itemView.imageView_bookmark_server
    private val maxImage = itemView.imageView_photomax_server
    private val icon_bar = itemView.linearLayout_image_icon_bar
    private val roomAddress: String = ServerPhotoRoomActivity.roomAddress!!
    private val likeCountText = itemView.textView_heart


    fun bindWithView(serverThumbnailPhotoModel: ServerThumbnailPhotoModel) {

        Log.d("TAG", "bindWithView: ${serverThumbnailPhotoModel.thumbnailPhoto}")
        Glide
            .with(App.instance)
            .load(serverThumbnailPhotoModel.thumbnailPhoto)
            .into(itemImage)

        likeCountText.text = serverThumbnailPhotoModel.likeCount.toString() + "개"


        if (serverThumbnailPhotoModel.userimg != null){
            Glide
                .with(App.instance)
                .load(serverThumbnailPhotoModel.userimg)
                .into(itemView.ProfileInPhotoRoom)
        }

        if (serverThumbnailPhotoModel.username != null){
            itemView.UsernameInPhotoRoom.text = serverThumbnailPhotoModel.username
        }

        CoroutineScope(Dispatchers.Main).launch {
            if (serverThumbnailPhotoModel.isLike) {
                favoriteImage.setImageResource(R.drawable.favorite_fill)
            } else {
                favoriteImage.setImageResource(R.drawable.favorite_2)
            }


            if (serverThumbnailPhotoModel.isPicked) {
                bookmarkImage.setImageResource(R.drawable.bookmark_fill)
            } else {
                bookmarkImage.setImageResource(R.drawable.bookmark_2)
            }
        }




        favoriteImage.setOnClickListener {
            if (serverThumbnailPhotoModel.isLike) { // 좋아요 해제
                CoroutineScope(Dispatchers.Main).launch {
                    favoriteImage.setImageResource(R.drawable.favorite_2)
                }
                serverThumbnailPhotoModel.isLike = false
                CoroutineScope(Dispatchers.IO).launch {
                    mSocket!!.emit(
                        "clickLike",
                        roomAddress,
                        adapterPosition,
                        serverThumbnailPhotoModel.pictureowner,
                        0
                    )
                }

            } else { // 좋아요 눌렀을때
                CoroutineScope(Dispatchers.Main).launch {
                    favoriteImage.setImageResource(R.drawable.favorite_fill)
                }
                serverThumbnailPhotoModel.isLike = true
                CoroutineScope(Dispatchers.IO).launch {
                    mSocket!!.emit(
                        "clickLike",
                        roomAddress,
                        adapterPosition,
                        serverThumbnailPhotoModel.pictureowner,
                        1
                    )
                }
            }
        }

        bookmarkImage.setOnClickListener {
            CoroutineScope(Dispatchers.Main).launch {
                if (serverThumbnailPhotoModel.isPicked) {
                    bookmarkImage.setImageResource(R.drawable.bookmark_2)
                    serverThumbnailPhotoModel.isPicked = false
                    photoPickedUriList.remove(serverThumbnailPhotoModel.thumbnailPhoto!!)
                    photoPickedList.remove(serverThumbnailPhotoModel)
                    serverFilePathList.add(serverThumbnailPhotoModel.absolutePath!!)
                } else {
                    bookmarkImage.setImageResource(R.drawable.bookmark_fill)
                    serverThumbnailPhotoModel.isPicked = true
                    photoPickedUriList.add(serverThumbnailPhotoModel.thumbnailPhoto!!)
                    photoPickedList.add(serverThumbnailPhotoModel)
                    serverFilePathList.remove(serverThumbnailPhotoModel.absolutePath!!)
                }
                delay(100)
                serverDrawerPickAdapter.notifyDataSetChanged()
            }
        }

        maxImage.setOnClickListener {


            var imagepath = serverThumbnailPhotoModel.thumbnailPhoto!!.getPath();
            var orientation =getOrientationOfImage(imagepath)

            Log.d("orientation", "bindWithView: ${orientation}")

            var intent = Intent(App.instance, ServerPhotoEnlargeActivity::class.java)
            serverThumbnailPhotoModel.thumbnailPhoto
            intent.putExtra("uri", serverThumbnailPhotoModel.thumbnailPhoto.toString())
            intent.putExtra("orientation", orientation)
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            App.instance.startActivity(intent)


        }


    }
}