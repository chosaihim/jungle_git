package com.example.pic_pho.WifiDirect.UI.WifiWaitingRoom

import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.WifiDirect.UI.PeerModel
import kotlinx.android.synthetic.main.item_wifi_waiting_room.view.*

class WifiWaitingViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
    private val waitingDeviceName = itemView.device_name_in_wifi_waiting_room

    fun bind(groupModel: PeerModel){
        waitingDeviceName.text = groupModel.deviceName
    }
}