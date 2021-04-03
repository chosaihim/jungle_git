package com.example.pic_pho.MakeGroup

import android.os.Build
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Filter
import android.widget.Filterable
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.App
import com.example.pic_pho.R
import kotlinx.android.synthetic.main.item_make_group_recycler.view.*

class MakeGroupRecyclerAdapter(makeGroupRecyclerViewInterface: MakeGroupRecyclerViewInterface) :
    RecyclerView.Adapter<MakeGroupViewHolder>(){
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
        holder.bind(this.modelList[position])

        holder.itemView.setOnClickListener {
            Toast.makeText(
                App.instance,
                "클릭됨!! ${position}",//"클릭됨!! ${this.modelList[position].name}",
                Toast.LENGTH_SHORT
            ).show()
//            holder.itemView.checkBox.toggle()

            if (this.modelList[position].isSelected == true) {
                this.modelList[position].isSelected = false
                holder.itemView.selected_radio_button.visibility = View.INVISIBLE
                holder.itemView.unselected_radio_button.visibility = View.VISIBLE


            } else {
                this.modelList[position].isSelected = true
                holder.itemView.selected_radio_button.visibility = View.VISIBLE
                holder.itemView.unselected_radio_button.visibility = View.INVISIBLE
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