package com.example.pic_pho.PhotoRoom

import android.net.Uri
import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import kotlinx.android.synthetic.main.photo_recycler_item.view.*

class ThumbnailViewHolder(
    itemView: View,
    recyclerViewInterface: ThumbnailRecyclerViewInterface
) :
    RecyclerView.ViewHolder(itemView) {

    val TAG: String = "로그"
    private val thumbnailPhotoView = itemView.thumbnailPhoto
    private var thumbnailRecyclerViewInterface: ThumbnailRecyclerViewInterface? = null
    private var sendUri: Uri? = null

    init {
        Log.d(TAG, "ThumbnailViewHolder - () called")

        this.thumbnailRecyclerViewInterface = recyclerViewInterface
    }

    // 데이터와 뷰를 묶는다.
    fun bind(thumbnailPhotoModel: ThumbnailPhotoModel) {
        sendUri = thumbnailPhotoModel.thumbnailPhoto
        Glide
            .with(App.instance)
            .load(thumbnailPhotoModel.thumbnailPhoto)
            .into(thumbnailPhotoView)
    }
}