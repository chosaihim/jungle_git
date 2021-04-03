package com.example.pic_pho.MakeGroup.selectedFriends

import android.util.Log
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.Toast
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.App
import com.example.pic_pho.R

class SelectedFriendsRecyclerAdapter(selectedFriendsRecyclerViewInterface: SelectedFriendsRecyclerViewInterface):
    RecyclerView.Adapter<SelectedFriendsViewHolder>() {

    val TAG: String = "로그"

    var modelList = ArrayList<SelectedFriendsModel>()

    //interface
    private var selectedFriendsRecyclerViewInterface: SelectedFriendsRecyclerViewInterface? = null

    init {
        this.selectedFriendsRecyclerViewInterface = selectedFriendsRecyclerViewInterface
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): SelectedFriendsViewHolder {
        return SelectedFriendsViewHolder(
            LayoutInflater.from(parent.context)
                .inflate(R.layout.item_selected_friends, parent, false),
            this.selectedFriendsRecyclerViewInterface!!
        )
    }

    override fun onBindViewHolder(holder: SelectedFriendsViewHolder, position: Int) {
        Log.d(TAG, "SelectedFriendsRecyclerAdapter - onBindViewHolder() called")
        holder.bind(this.modelList[position])

        holder.itemView.setOnClickListener {
            Toast.makeText(
                App.instance,
                "클릭됨!! ${position}",//"클릭됨!! ${this.modelList[position].name}",
                Toast.LENGTH_SHORT
            ).show()
        }

    }

    override fun getItemCount(): Int {
        return this.modelList.size
    }

    fun submitList(modelList: ArrayList<SelectedFriendsModel>) {
        this.modelList = modelList
    }

}
