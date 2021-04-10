package com.example.pic_pho.MakeGroup

import android.os.Build
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.App
import com.example.pic_pho.MakeGroup.MakeGroupActivity.Companion.selectedFriendsModelList
import com.example.pic_pho.MakeGroup.MakeGroupActivity.Companion.selectedFriendsRecyclerAdapter
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsModel
import com.example.pic_pho.R
import kotlinx.android.synthetic.main.item_make_group_recycler.view.*
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MakeGroupRecyclerAdapter(makeGroupRecyclerViewInterface: MakeGroupRecyclerViewInterface) :
    RecyclerView.Adapter<MakeGroupViewHolder>() {
    val TAG: String = "로그"

    var modelList = ArrayList<MakeGroupModel>()

    //interface
    private var makeGroupRecyclerViewInterface: MakeGroupRecyclerViewInterface? = null

    init {
        this.makeGroupRecyclerViewInterface = makeGroupRecyclerViewInterface
    }


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MakeGroupViewHolder {
        return MakeGroupViewHolder(
            LayoutInflater.from(parent.context)
                .inflate(R.layout.item_make_group_recycler, parent, false),
            this.makeGroupRecyclerViewInterface!!
        )

    }

    @RequiresApi(Build.VERSION_CODES.Q)
    override fun onBindViewHolder(holder: MakeGroupViewHolder, position: Int) {
        Log.d(TAG, "MakeGroupRecyclerAdapter - onBindViewHolder() called")
        holder.bind(modelList[position])

        CoroutineScope(Dispatchers.Main).launch {
            delay(100)
            if (modelList[position].isOnline != 1) {
                holder.itemView.setOnClickListener {
                    Toast.makeText(
                        App.instance,
                        "클릭됨!! ${position}",//"클릭됨!! ${this.modelList[position].name}",
                        Toast.LENGTH_SHORT
                    ).show()
//            holder.itemView.checkBox.toggle()

                    if (modelList[position].isSelected == true) {
                        modelList[position].isSelected = false
                        holder.itemView.selected_radio_button.visibility = View.INVISIBLE
                        holder.itemView.unselected_radio_button.visibility = View.VISIBLE

                        for (model in selectedFriendsModelList) {
                            if (modelList[position].profileImage == model.profileImage) {
                                selectedFriendsModelList.remove(model)
                                break
                            }
                        }
                        selectedFriendsRecyclerAdapter.notifyDataSetChanged()

                        if (selectedFriendsModelList.size == 0) {
                            MakeGroupActivity.selectedFriends!!.visibility = View.GONE
                        }

                        Log.e(TAG, "셀렉티드프렌즈모델리스트 지울 때: ${selectedFriendsModelList}")

                    } else {
                        modelList[position].isSelected = true
                        holder.itemView.selected_radio_button.visibility = View.VISIBLE
                        holder.itemView.unselected_radio_button.visibility = View.INVISIBLE

                        var selectedFriendsModel =
                            SelectedFriendsModel(modelList[position].profileImage.toString())
                        MakeGroupActivity.selectedFriendsModelList.add(selectedFriendsModel)
                        Log.e(TAG, "셀렉티드프렌즈모델리스트: ${selectedFriendsModelList}")
                        selectedFriendsRecyclerAdapter.notifyDataSetChanged()

                        MakeGroupActivity.selectedFriends!!.visibility = View.VISIBLE
                    }
                }
            }
        }

    }

    override fun getItemCount(): Int {
        return this.modelList.size

    }

    fun submitList(modelList: ArrayList<MakeGroupModel>) {
        this.modelList = modelList
    }


}