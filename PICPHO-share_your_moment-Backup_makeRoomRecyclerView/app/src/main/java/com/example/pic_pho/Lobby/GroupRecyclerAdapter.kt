package com.example.pic_pho.Lobby

import android.app.Activity
import android.content.Intent
import android.provider.MediaStore
import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.Button
import android.widget.Toast
import androidx.core.app.ActivityCompat.startActivity
import androidx.core.app.ActivityCompat.startActivityForResult
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.App
import com.example.pic_pho.R
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import java.net.URISyntaxException
import kotlin.concurrent.thread

class GroupRecyclerAdapter : RecyclerView.Adapter<GroupViewHolder>() {

    private val TAG = "GroupRecyclerAdapter"
    private var modelList = ArrayList<GroupModel>()

    //뷰홀더가 생성되었을 때
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): GroupViewHolder {
        return GroupViewHolder(
            LayoutInflater.from(parent.context).inflate(
                R.layout.group_recycler_item,
                parent,
                false
            )
        )
    }

    //목록의 아이템 개
    override fun getItemCount(): Int {
        return this.modelList.size
    }

    //뷰와 뷰홀더가 묶였을 때
    override fun onBindViewHolder(holder: GroupViewHolder, position: Int) {
        Log.d(TAG, "GroupRecyclerAdapter - onBindViewHolder() called / position: $position")
        holder.bind(this.modelList[position])

        //클릭 설정
        holder.itemView.setOnClickListener {

        //어뎁터에서 액티비티 화면전환!!

            val intent = Intent(App.instance, ServerPhotoRoomActivity::class.java)
            intent.putExtra("channel", modelList[position].name)
            App.instance.startActivity(intent)
        }
    }

    //외부에서 데이터 넘기기
    fun submitList(modelList: ArrayList<GroupModel>) {
        this.modelList = modelList
    }

}