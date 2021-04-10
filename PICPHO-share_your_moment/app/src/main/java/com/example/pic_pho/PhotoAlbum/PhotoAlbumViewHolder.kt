package com.example.pic_pho.PhotoAlbum

import android.net.Uri
import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.R
import kotlinx.android.synthetic.main.item_photo_album.view.*
import java.io.File

class PhotoAlbumViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private var albumImage = itemView.photo_album_item_image


//    fun bindWithView(photoAlbumPageItemModel: PhotoAlbumPageItemModel) {
//        val uriPhotoAlbum = Uri.parse(photoAlbumPageItemModel.absolutePath)
//        Glide
//            .with(App.instance)
//            .load(uriPhotoAlbum)
//            .into(itemImage)
//    }
    fun bindWithView(photoUri: Uri) {

//        Log.d("TAG", "bindWithView !!!!!!!!!!!!!!!!!!!!!!! : ${photoUri}, ${albumImage}, ${uri}")

        Glide
            .with(App.instance)
            .load(photoUri)
            .into(albumImage)
    }
}