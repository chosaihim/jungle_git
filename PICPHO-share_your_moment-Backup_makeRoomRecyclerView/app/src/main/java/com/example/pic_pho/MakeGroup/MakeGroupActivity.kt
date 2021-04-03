package com.example.pic_pho.MakeGroup

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.pic_pho.App
import com.example.pic_pho.CellularSocket.SocketUtill
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsModel
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsRecyclerAdapter
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsRecyclerViewInterface
import com.example.pic_pho.PhotoRoomServer.ServerPhotoRoomActivity
import com.example.pic_pho.databinding.ActivityMakeGroupBinding
import com.github.nkzawa.socketio.client.Socket
import com.google.firebase.iid.FirebaseInstanceId
import com.google.gson.JsonArray
import com.google.gson.JsonObject
import com.kakao.sdk.talk.TalkApiClient
import com.kakao.sdk.user.UserApiClient
import kotlinx.android.synthetic.main.activity_lobby.*
import kotlinx.android.synthetic.main.activity_login.*
import kotlinx.android.synthetic.main.activity_make_group.*
import kotlinx.android.synthetic.main.activity_photoroom.*
import kotlinx.android.synthetic.main.item_make_group_recycler.*
import kotlinx.android.synthetic.main.item_selected_friends.*
import java.net.URISyntaxException


class MakeGroupActivity : AppCompatActivity(),
    MakeGroupRecyclerViewInterface, SelectedFriendsRecyclerViewInterface {

    val TAG: String = "로그"
    lateinit var binding: ActivityMakeGroupBinding

    var makeGroupModelList = ArrayList<MakeGroupModel>()

    private lateinit var makeGroupRecyclerAdapter: MakeGroupRecyclerAdapter
    var mSocket: Socket? = null

    companion object{
        var selectedFriendsModelList = ArrayList<SelectedFriendsModel>()
        lateinit var selectedFriendsRecyclerAdapter: SelectedFriendsRecyclerAdapter

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)


        //선택된 친구들 selected Friends
        selectedFriendsRecyclerAdapter= SelectedFriendsRecyclerAdapter(this)


        TalkApiClient.instance.friends { friends, error ->
            if (error != null) {
                Log.e(TAG, "카카오톡 친구 목록 가져오기 실패", error)
            } else if (friends != null) {
                Log.i(TAG, "카카오톡 친구 목록 가져오기 성공 \n${friends.elements.joinToString("\n")}")
                // 친구의 UUID 로 메시지 보내기 가능

                binding = ActivityMakeGroupBinding.inflate(layoutInflater)
                setContentView(binding.root)

                for (i in 0 until friends.elements.size) {
                    var groupModel = MakeGroupModel(
                        name = friends.elements[i].profileNickname,
                        profileImage = friends.elements[i].profileThumbnailImage.toString(),
                        userId = friends.elements[i].id.toInt()
                    )
                    makeGroupModelList.add(groupModel)

                }

                //test
                for (i in 0..3){
                    for (i in 0 until friends.elements.size) {

                        var selectedFriendsModel =
                            SelectedFriendsModel(friends.elements[i].profileThumbnailImage.toString())
                        selectedFriendsModelList.add(selectedFriendsModel)
                    }
                }
                //어댑터 인스턴스 생성
                makeGroupRecyclerAdapter = MakeGroupRecyclerAdapter(this)
                makeGroupRecyclerAdapter.submitList(makeGroupModelList)

                friend_list.apply {
                    layoutManager =
                        LinearLayoutManager(
                            this@MakeGroupActivity,
                            LinearLayoutManager.VERTICAL,
                            false
                        )
                    adapter = makeGroupRecyclerAdapter
                }


                //selectedFriends 어댑터 인스턴스 생성
//                selectedFriendsRecyclerAdapter = SelectedFriendsRecyclerAdapter(this)
                selectedFriendsRecyclerAdapter.submitList(selectedFriendsModelList)

                selected_friends.apply{

                    layoutManager =
                        LinearLayoutManager(
                            this@MakeGroupActivity,
                            LinearLayoutManager.HORIZONTAL,
                            false
                        )
                    adapter = selectedFriendsRecyclerAdapter

                }

            }
        }

//
//        binding.searchviewMakegroup.setOnQueryTextListener(object : SearchView.OnQueryTextListener {
//            override fun onQueryTextSubmit(p0: String?): Boolean {
//                return true
//            }
//
//            override fun onQueryTextChange(p0: String?): Boolean {
//                binding.textTestSearchView.text = p0
//                return true
//            }
//
//        })

    }

    fun sendAlarm(view: View) {
        try {

            mSocket = SocketUtill.createAndConnetSocket()
            mSocket!!.emit("push_send", 1)

            val token = FirebaseInstanceId.getInstance().token
            Log.e(TAG, "token: ${token}")

        } catch (e: URISyntaxException) {
            Log.d(TAG, "failed")
        }
    }

    //function for finish action
    fun makeGroupAction(view: View) {

        Toast.makeText(
            App.instance,
            "그룹만들기!!",//"클릭됨!! ${this.modelList[position].name}",
            Toast.LENGTH_SHORT
        ).show()

        //TODO 본인 정보도 포함 시켜서 보내야함
        mSocket = SocketUtill.createAndConnetSocket()
        if (mSocket != null) {
            var selecetedModelList = ArrayList<MakeGroupModel>()
            var jsonobjectlist: JsonArray = JsonArray()
            for (i in 0 until makeGroupModelList.size) {
                if (makeGroupModelList[i].isSelected == true) {
                    var jsonobject: JsonObject? = JsonObject()
                    jsonobject!!.addProperty("userid", makeGroupModelList[i].userId.toString())
                    jsonobject!!.addProperty("name", makeGroupModelList[i].name.toString())
                    jsonobject!!.addProperty(
                        "profileImage",
                        makeGroupModelList[i].profileImage.toString()
                    )
                    jsonobjectlist.add(jsonobject)
                }
            }


            UserApiClient.instance.me { user, error ->
                if (error != null) {
                    Log.e(TAG, "사용자 정보 요청 실패", error)
                } else if (user != null) {
                    Log.i(TAG, "사용자 정보 요청 성공")
                    Log.d("jsonobject", "makeGroupAction: ${jsonobjectlist}")
                    mSocket!!.emit("selectedGroup", jsonobjectlist, "picpho" + user.id.toString())

                    val intent:Intent = Intent(this, ServerPhotoRoomActivity::class.java)
                    intent.putExtra("roomAddress", "picpho" + user.id.toString())
                    intent.putExtra("numOfMembers", jsonobjectlist.size())
                    Log.e("로그", intent.getStringExtra("roomAddress"))
//                    Toast.makeText(this, "${intent.getStringExtra("roomAddress")}", Toast.LENGTH_SHORT).show()
                    startActivity(intent)
                }

            }


        } else {
            Log.d(TAG, "makeGroupAction: socket null")
        }



    }

    override fun onItemClicked() {
    }

    override fun onDestroy() {
        super.onDestroy()
        if (mSocket != null) {
            mSocket!!.close()
        }
    }

}

