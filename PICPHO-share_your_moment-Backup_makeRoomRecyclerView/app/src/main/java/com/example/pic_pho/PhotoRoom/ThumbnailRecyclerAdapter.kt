package com.example.pic_pho.PhotoRoom

import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.R

class ThumbnailRecyclerAdapter(ThumbnailRecyclerViewInterface: ThumbnailRecyclerViewInterface): RecyclerView.Adapter<ThumbnailViewHolder>() {


    private var photoModelList = ArrayList<ThumbnailPhotoModel>()
    private val TAG = "ThumbnailRecyclerAdapter"
    //인터페이스 추가 ****
    //interface
    private var ThumbnailRecyclerViewInterface: ThumbnailRecyclerViewInterface? = null

    //생성자
    init{
        this.ThumbnailRecyclerViewInterface = ThumbnailRecyclerViewInterface
    }
    
    //인터페이스 추가 완료 ****

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ThumbnailViewHolder {
        return ThumbnailViewHolder(LayoutInflater.from(parent.context)
            .inflate(R.layout.photo_recycler_item, parent, false),
            this.ThumbnailRecyclerViewInterface!!)
        //느낌표 두개: 값이 꼭 있을 거라고 가정하고 넣은 것임!
    }

    override fun onBindViewHolder(holder: ThumbnailViewHolder, position: Int) {
        holder.bind(this.photoModelList[position])

        holder.itemView.setOnClickListener {
            PhotoRoomActivity.changeSelectedPhotoByClicked(position)
        }


        Log.d(TAG, "onBindViewHolder: ${this.photoModelList[position]}")
    }

    override fun getItemCount(): Int {
        return this.photoModelList.size
    }

    fun submitList(photoModelListServer: ArrayList<ThumbnailPhotoModel>){
        this.photoModelList = photoModelListServer
    }
}