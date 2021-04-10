package com.example.pic_pho.WaitingRoomServer

import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import kotlinx.android.synthetic.main.item_waiting_room_server.view.*

class ServerWaitingRoomHolder(itemView: View) : RecyclerView.ViewHolder(itemView){
    private val TAG = "ServerWaitingRoomHolder"
    // 데이터와 뷰를 묶는다.
    fun bind(serverWaitingRoomModel: ServerWaitingRoomActivity.GroupMember) {

        itemView.member_name_server.text = serverWaitingRoomModel.NickName.toString()

        when (serverWaitingRoomModel.status) {
            0 -> {
                itemView.wifi_progress_cloud_imageview.visibility = View.VISIBLE
                itemView.wifi_progress_cloud_ing_imageview.visibility = View.INVISIBLE
                itemView.wifi_progress_cloud_done_imageview.visibility = View.INVISIBLE
            }
            1 -> {
                itemView.wifi_progress_cloud_imageview.visibility = View.INVISIBLE
                itemView.wifi_progress_cloud_ing_imageview.visibility = View.VISIBLE
                itemView.wifi_progress_cloud_done_imageview.visibility = View.INVISIBLE
            }
            2 -> {
                itemView.wifi_progress_cloud_imageview.visibility = View.INVISIBLE
                itemView.wifi_progress_cloud_ing_imageview.visibility = View.INVISIBLE
                itemView.wifi_progress_cloud_done_imageview.visibility = View.VISIBLE
            }
        }

        Log.d(TAG, "bind: ${itemView.member_name_server.text}")
        Glide
            .with(App.instance)
            .load(serverWaitingRoomModel.ProfileUrl)
            .into(itemView.profilephoto_in_waiting_room_server)
    }
}