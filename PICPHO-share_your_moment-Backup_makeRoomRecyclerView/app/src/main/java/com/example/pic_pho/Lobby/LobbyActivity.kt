package com.example.pic_pho.Lobby

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.MakeGroup.MakeGroupActivity
import com.example.pic_pho.R
import com.example.pic_pho.databinding.ActivityLobbyBinding
import kotlinx.android.synthetic.main.activity_lobby.*
import kotlinx.android.synthetic.main.group_recycler_item.*
import kotlinx.android.synthetic.main.group_recycler_item.view.*

class LobbyActivity : AppCompatActivity() {

    val TAG: String = "로그"

    val GroupName : String = "정훈동창모임"

    //데이터를 담을 그릇
    var modelList = ArrayList<GroupModel>()

    private lateinit var myRecyclerAdapter: GroupRecyclerAdapter
    private lateinit var binding: ActivityLobbyBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLobbyBinding.inflate(layoutInflater)
        setContentView(binding.root)

        Log.d(TAG, "onCreate: called")
        Log.d(TAG, "돌리기 전: ${this.modelList.size}")

        for(i in 1..10){
            val groupModel = GroupModel(name = "$GroupName $i", profileImage = "https://img.tvreportcdn.de/cms-content/uploads/2020/09/01/75d6b835-c759-42ca-b753-f941121e9ba6.jpg")
            this.modelList.add(groupModel)

        }
        Log.d(TAG, "돌리기 후: ${this.modelList.size}")

        //어댑터 인스턴스 생성
        myRecyclerAdapter = GroupRecyclerAdapter()
        myRecyclerAdapter.submitList(this.modelList)

        //리사이클러뷰 설정
        binding.groupRecyclerView.apply{
            layoutManager = LinearLayoutManager(this@LobbyActivity, LinearLayoutManager.VERTICAL, false)
            //어답터 장착
            adapter = myRecyclerAdapter
        }

        binding.floatingActionButtonLobby.setOnClickListener {
            val intent = Intent(this, MakeGroupActivity::class.java)
            startActivity(intent)
        }
    }

    fun clickSearchView(view : View){
        if(binding.searchviewLobby.visibility == View.VISIBLE){
            binding.searchviewLobby.visibility = View.GONE
        }else{
            binding.searchviewLobby.visibility = View.VISIBLE
        }
    }

}