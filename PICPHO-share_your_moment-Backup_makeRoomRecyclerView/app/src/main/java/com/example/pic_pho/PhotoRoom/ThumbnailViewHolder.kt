package com.example.pic_pho.PhotoRoom

import android.net.Uri
import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import kotlinx.android.synthetic.main.photo_recycler_item.view.*

class ThumbnailViewHolder(itemView: View,
                          recyclerViewInterfaceServer: ThumbnailRecyclerViewInterface
):
                            RecyclerView.ViewHolder(itemView)
    {

    val TAG: String = "로그"

    private val thumbnailPhotoView = itemView.thumbnailPhoto

    private var ThumbnailRecyclerViewInterface: ThumbnailRecyclerViewInterface? = null

    private var sendUri : Uri? = null

    init {
        Log.d(TAG, "ThumbnailViewHolder - () called")

        this.ThumbnailRecyclerViewInterface = recyclerViewInterfaceServer
    }

    // 데이터와 뷰를 묶는다.
    fun bind(ThumbnailPhotoModel: ThumbnailPhotoModel){
        sendUri = ThumbnailPhotoModel.thumbnailPhoto
        Glide
            .with(App.instance)
            .load(ThumbnailPhotoModel.thumbnailPhoto)
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