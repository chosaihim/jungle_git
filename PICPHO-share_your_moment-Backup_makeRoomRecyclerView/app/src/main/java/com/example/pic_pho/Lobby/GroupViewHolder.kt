package com.example.pic_pho.Lobby

import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.R
import kotlinx.android.synthetic.main.group_recycler_item.view.*

class GroupViewHolder(itemView: View):RecyclerView.ViewHolder(itemView) {
    val TAG: String = "로그"

    private val usernameTextView = itemView.textView_group_name

    //기본 생성자
    init {
        Log.d(TAG, "GroupViewHolder - () called")
    }

    //데이터와 뷰를 묶는다.
    fun bind(groupModel: GroupModel){
        Log.d(TAG, "GroupViewHolder - bind() called")

        usernameTextView.text = groupModel.name
    }
}