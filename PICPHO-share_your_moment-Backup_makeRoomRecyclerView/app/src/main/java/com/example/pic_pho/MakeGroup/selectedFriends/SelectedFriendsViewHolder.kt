package com.example.pic_pho.MakeGroup.selectedFriends

import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.R
import kotlinx.android.synthetic.main.item_selected_friends.view.*

class SelectedFriendsViewHolder(
    itemView: View,
    recyclerViewInterface: SelectedFriendsRecyclerViewInterface
) :
    RecyclerView.ViewHolder(itemView),
    View.OnClickListener {

    private val TAG = "SelectedFriendsViewHolder"
    private var selectedFriendsRecyclerViewInterface: SelectedFriendsRecyclerViewInterface? = null

    init {
        Log.d(TAG, "init() called")

        //interface
        itemView.setOnClickListener(this)
        this.selectedFriendsRecyclerViewInterface = recyclerViewInterface
    }

    // 데이터와 뷰를 묶는다.
    fun bind(selectedFriendsModel: SelectedFriendsModel) {
        Log.d(TAG, "SelectedFriendsViewHolder - bind() called")


        Glide
            .with(App.instance)
            .load(selectedFriendsModel.profileImage)
            .placeholder(R.drawable.picpho_logo)
            .into(itemView.imageview_selected_friend)


    }


    override fun onClick(p0: View?) {
        Log.d(TAG, "SelectedFriendsViewHolder - onClick() called")

        //interface
        itemView.setOnClickListener(this)
        this.selectedFriendsRecyclerViewInterface?.onItemClicked()

    }


}