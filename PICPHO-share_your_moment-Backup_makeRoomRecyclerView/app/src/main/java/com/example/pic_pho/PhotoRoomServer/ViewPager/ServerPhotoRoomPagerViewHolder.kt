package com.example.pic_pho.PhotoRoomServer.ViewPager

import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.PhotoRoomServer.ServerThumbnailPhotoModel
import kotlinx.android.synthetic.main.item_photoroom_pager.view.*

class ServerPhotoRoomPagerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val itemImage = itemView.SelectedPhoto

    fun bindWithView(serverThumbnailPhotoModel: ServerThumbnailPhotoModel) {
        Glide
            .with(App.instance)
            .load(serverThumbnailPhotoModel.thumbnailPhoto)
//            .placeholder(R.drawable.picpho_logo)
            .into(itemImage)
    }
}