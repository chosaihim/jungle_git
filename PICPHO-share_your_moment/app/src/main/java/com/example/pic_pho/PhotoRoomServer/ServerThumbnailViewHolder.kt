package com.example.pic_pho.PhotoRoomServer

import android.net.Uri
import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import kotlinx.android.synthetic.main.photo_recycler_item.view.*

class ServerThumbnailViewHolder(itemView: View,
                                recyclerViewInterfaceServer: ServerThumbnailRecyclerViewInterface
):
    RecyclerView.ViewHolder(itemView)
{
    val TAG: String = "로그"

    private val thumbnailPhotoView = itemView.thumbnailPhoto

    private var serverThumbnailRecyclerViewInterface: ServerThumbnailRecyclerViewInterface? = null

    private var sendUri : Uri? = null

    init {
        Log.d(TAG, "ThumbnailViewHolder - () called")

        this.serverThumbnailRecyclerViewInterface = recyclerViewInterfaceServer
    }

    // 데이터와 뷰를 묶는다.
    fun bind(serverThumbnailPhotoModel: ServerThumbnailPhotoModel){
//        sendUri = serverThumbnailPhotoModel.thumbnailPhoto
        Glide
            .with(App.instance)
            .load(serverThumbnailPhotoModel.thumbnailPhoto)
//            .load(R.drawable.my)
//            .centerCrop()
//            .placeholder(R.drawable.picpho_logo)
            .into(thumbnailPhotoView)
    }

//        override fun onClick(p0: View?) {
//            Log.d(TAG, "ThumbnailViewHolder - onClick() called")
//
//            //interface
//            itemView.setOnClickListener(this)
//            this.thumbnailRecyclerViewInterface?.onItemClicked(sendUri!!)
//        }
}

