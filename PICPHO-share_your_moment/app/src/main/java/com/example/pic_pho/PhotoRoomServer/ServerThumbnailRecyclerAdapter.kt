package com.example.pic_pho.PhotoRoomServer

import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.PhotoRoomServer.ServerThumbnailPhotoModel
import com.example.pic_pho.PhotoRoomServer.ServerThumbnailRecyclerViewInterface
import com.example.pic_pho.PhotoRoomServer.ServerThumbnailViewHolder
import com.example.pic_pho.R

class ServerThumbnailRecyclerAdapter(serverThumbnailRecyclerViewInterface: ServerThumbnailRecyclerViewInterface): RecyclerView.Adapter<ServerThumbnailViewHolder>() {


    private var photoModelList = ArrayList<ServerThumbnailPhotoModel>()
    private val TAG = "ThumbnailRecyclerAdapter"

    //인터페이스 추가 ****
    //interface
    private var serverThumbnailRecyclerViewInterface: ServerThumbnailRecyclerViewInterface? = null

    //생성자
    init{
        this.serverThumbnailRecyclerViewInterface = serverThumbnailRecyclerViewInterface
    }
    //인터페이스 추가 완료 ****



    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ServerThumbnailViewHolder {
        return ServerThumbnailViewHolder(LayoutInflater.from(parent.context)
            .inflate(R.layout.photo_recycler_item, parent, false),
            this.serverThumbnailRecyclerViewInterface!!)
        //느낌표 두개: 값이 꼭 있을 거라고 가정하고 넣은 것임!
    }



    override fun onBindViewHolder(holderServer: ServerThumbnailViewHolder, position: Int) {
        holderServer.bind(this.photoModelList[position])

        holderServer.itemView.setOnClickListener {
            ServerPhotoRoomActivity.changeSelectedPhotoByClicked(position)
        }


        Log.d(TAG, "onBindViewHolder: ${this.photoModelList[position]}")
    }

    override fun getItemCount(): Int {
        return this.photoModelList.size
    }

    fun submitList(photoModelListServer: ArrayList<ServerThumbnailPhotoModel>){
        this.photoModelList = photoModelListServer
    }
}