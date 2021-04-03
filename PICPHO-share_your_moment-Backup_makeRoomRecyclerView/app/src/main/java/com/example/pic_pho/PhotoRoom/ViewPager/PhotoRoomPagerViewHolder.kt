package com.example.pic_pho.PhotoRoom.ViewPager

import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.PhotoRoom.ThumbnailPhotoModel
import kotlinx.android.synthetic.main.item_photoroom_pager.view.*

class PhotoRoomPagerViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val itemImage = itemView.SelectedPhoto

    fun bindWithView(ThumbnailPhotoModel: ThumbnailPhotoModel) {
        Glide
            .with(App.instance)
            .load(ThumbnailPhotoModel.thumbnailPhoto)
//            .placeholder(R.drawable.picpho_logo)
            .into(itemImage)
    }
}