package com.example.pic_pho.MakeGroup

import android.util.Log
import android.view.View
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide
import com.example.pic_pho.App
import com.example.pic_pho.R
import kotlinx.android.synthetic.main.item_make_group_recycler.view.*

class MakeGroupViewHolder(
    itemView: View,
    recyclerViewInterface: MakeGroupRecyclerViewInterface
) :
    RecyclerView.ViewHolder(itemView),
    View.OnClickListener {

    private val TAG = "MakeGroupViewHolder"
    private val makeGroupView = itemView.make_group_profile
    private var makeGroupRecyclerViewInterface: MakeGroupRecyclerViewInterface? = null

    init {
        Log.d(TAG, "MakeGroupViewHolder - () called")

        //interface
        itemView.setOnClickListener(this)
        this.makeGroupRecyclerViewInterface = recyclerViewInterface
    }

    // 데이터와 뷰를 묶는다.
    fun bind(makeGroupModel: MakeGroupModel) {
        Log.d(TAG, "MakeGroupViewHold er - bind() called")

        itemView.make_group_name.text = makeGroupModel.name

        if(makeGroupModel.isOnline == 1){
            itemView.unselected_radio_button.setImageResource(R.drawable.ic_baseline_radio_button_online_24)
        }

        Glide
            .with(App.instance)
            .load(makeGroupModel.profileImage)
            .into(itemView.make_group_profile)
    }


    override fun onClick(p0: View?) {
        Log.d(TAG, "MakeGroupViewHolder - onClick() called")

        //interface
        itemView.setOnClickListener(this)
        this.makeGroupRecyclerViewInterface?.onItemClicked()
//        itemView.checkBox.toggle()


//        if(itemView.checkBox.isSelected == true){
//            modelList[1].isSelected
//        }else{
//            makeGroupModel.isSelected
//        }

    }


}