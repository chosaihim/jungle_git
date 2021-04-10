package com.example.pic_pho.MakeGroup

import android.app.Activity
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.App
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.createAndConnectSocket
import com.example.pic_pho.CellularSocket.SocketUtil.Companion.mSocket
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsModel
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsRecyclerAdapter
import com.example.pic_pho.MakeGroup.selectedFriends.SelectedFriendsRecyclerViewInterface
import com.example.pic_pho.WaitingRoomServer.ServerWaitingRoomActivity
import com.example.pic_pho.WifiDirect.UI.HorizontalItemDecoration
import com.example.pic_pho.databinding.ActivityMakeGroupBinding
import com.github.nkzawa.emitter.Emitter
import com.google.gson.Gson
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
import kotlinx.coroutines.*
import org.jetbrains.anko.toast
import org.json.JSONArray


class MakeGroupActivity : AppCompatActivity(),
    MakeGroupRecyclerViewInterface, SelectedFriendsRecyclerViewInterface {

    val TAG: String = "로그"
    lateinit var binding: ActivityMakeGroupBinding

    var makeGroupModelList = ArrayList<MakeGroupModel>()

    private lateinit var makeGroupRecyclerAdapter: MakeGroupRecyclerAdapter

    companion object {
        lateinit var invitedFriendsJsonArray: JsonArray

        var selectedFriends: RecyclerView? = null

        var selectedFriendsModelList = ArrayList<SelectedFriendsModel>()
        lateinit var selectedFriendsRecyclerAdapter: SelectedFriendsRecyclerAdapter

        //수정(jsonObject없이 수정)
        var selectedFriendsList = ArrayList<MakeGroupModel>()
        var makeGroupActivity: Activity? = null
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        makeGroupActivity = this

        binding = ActivityMakeGroupBinding.inflate(layoutInflater)
        setContentView(binding.root)
        selectedFriends = binding.selectedFriends

        if (mSocket == null) {
            Log.d(TAG, "onCreate: 온크리에이트에서 소켓 연결 시도 함 ㅋㅋ")
            mSocket = createAndConnectSocket()
        }

        CoroutineScope(Dispatchers.IO).launch {
            mSocket!!.on("kakaoFriendsOnlineReturn", parseMakeGroupModelList)
            delay(200)
        }

        selectedFriendsModelList.clear()
        selectedFriendsList.clear()
        makeGroupModelList.clear()

        //어댑터 인스턴스 생성
        makeGroupRecyclerAdapter = MakeGroupRecyclerAdapter(this)
        makeGroupRecyclerAdapter.submitList(makeGroupModelList)

        binding.friendList.apply {
            layoutManager =
                LinearLayoutManager(
                    this@MakeGroupActivity,
                    LinearLayoutManager.VERTICAL,
                    false
                )
            adapter = makeGroupRecyclerAdapter
        }


        //selectedFriends 어댑터 인스턴스 생성
        selectedFriendsRecyclerAdapter = SelectedFriendsRecyclerAdapter(this)
        selectedFriendsRecyclerAdapter.submitList(selectedFriendsModelList)
        update_selectedFriends_recyclerview()


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

    override fun onStart() {
        super.onStart()

    }

    override fun onResume() {
        super.onResume()
        if (mSocket == null) {
            Log.d(TAG, "onResume: 온리줌에서 소켓 연결 시도 함 ㅋㅋ")
            mSocket = createAndConnectSocket()
        }

        TalkApiClient.instance.friends { friends, error ->
            if (error != null) {
                Log.e(TAG, "카카오톡 친구 목록 가져오기 실패", error)
            } else if (friends != null) {
                Log.i(TAG, "카카오톡 친구 목록 가져오기 성공 \n${friends.elements.joinToString("\n")}")
                // 친구의 UUID 로 메시지 보내기 가능

                var kakaoFriendsList = JSONArray()

                for (i in 0 until friends.elements.size) {
                    var kakaoFriend = JsonObject()
                    kakaoFriend.apply {
                        addProperty("name", friends.elements[i].profileNickname)
                        addProperty(
                            "profileImage",
                            friends.elements[i].profileThumbnailImage.toString()
                        )
                        addProperty("userId", friends.elements[i].id.toInt())
                    }
                    kakaoFriendsList.put(kakaoFriend)
                }
                Log.e(TAG, "onCreate: kakaoFriendsList 111  ${kakaoFriendsList}", )
                mSocket!!.emit("CheckFriendsOnline", kakaoFriendsList.toString())
            }
        }

    }

    var parseMakeGroupModelList = Emitter.Listener {
        Log.d(TAG, "parseMakeGroupModelList: parseMakeGroupModelList")
        var kakaoFriendsList = it[0].toString()
        var jsonArray = JSONArray(kakaoFriendsList)
        val gson = Gson()
        for (i in 0 until jsonArray.length()) {
            var groupModel = gson.fromJson(jsonArray[i].toString(), MakeGroupModel::class.java)
            makeGroupModelList.add(groupModel)
            Log.e(TAG, "parseMakeGroupModelList: ${groupModel}")
        }
        Log.d(TAG, "파스 메이크 그룹 모델 리스트 에서 : $makeGroupModelList")
        makeGroupAdapterNotifiDataSetChanged()
    }

    fun makeGroupAdapterNotifiDataSetChanged() {
        CoroutineScope(Dispatchers.Main).launch {
            delay(100)
            makeGroupRecyclerAdapter.notifyDataSetChanged()
        }
    }


    fun update_selectedFriends_recyclerview() {
        binding.selectedFriends.apply {
            layoutManager =
                LinearLayoutManager(
                    this@MakeGroupActivity,
                    LinearLayoutManager.HORIZONTAL,
                    false
                )
            adapter = selectedFriendsRecyclerAdapter
            addItemDecoration(HorizontalItemDecoration(20))
        }
    }


    fun activityfinish(view: View) {
        finish()
    }


    //function for finish action
    fun makeGroupAction(view: View) {
        //그룹방 이름 받아오기
        val roomName = binding.edittextRoomname.text.toString()
        Log.e(TAG, "그룹방 이름: ${roomName}")

        if (roomName.isEmpty()) {
            //방 이름이 공백일 때!
            Toast.makeText(
                App.instance,
                "방 이름을 입력해주세요.",
                Toast.LENGTH_SHORT
            ).show()

            return
        }
        //디버깅용
        else {
            //방 이름이 있을 때!

            Toast.makeText(
                App.instance,
                "그룹만들기!!",//"클릭됨!! ${this.modelList[position].name}",
                Toast.LENGTH_SHORT
            ).show()
        }


        //TODO 본인 정보도 포함 시켜서 보내야함

        if (mSocket != null) {
            invitedFriendsJsonArray = JsonArray()
            for (i in 0 until makeGroupModelList.size) {
                if (makeGroupModelList[i].isSelected == true) {
                    var jsonobject: JsonObject? = JsonObject()
                    jsonobject!!.addProperty("userid", makeGroupModelList[i].userId.toString())
                    jsonobject!!.addProperty("name", makeGroupModelList[i].name.toString())
                    jsonobject!!.addProperty(
                        "profileImage",
                        makeGroupModelList[i].profileImage.toString()
                    )
                    jsonobject!!.addProperty("roomName", roomName)
                    invitedFriendsJsonArray.add(jsonobject)

                    selectedFriendsList.add(makeGroupModelList[i])
                }
            }

            if(selectedFriendsList.size < 1){
                toast("초대할 친구를 선택해주세요")
                return
            }

            UserApiClient.instance.me { user, error ->
                if (error != null) {
                    Log.e(TAG, "사용자 정보 요청 실패", error)
                } else if (user != null) {
                    Log.i(TAG, "사용자 정보 요청 성공")
                    Log.d("jsonobject", "makeGroupAction: ${invitedFriendsJsonArray}")
                    mSocket!!.emit(
                        "selectedGroup",
                        invitedFriendsJsonArray,
                        "picpho" + user.id.toString(),
                        roomName
                    )

                    var roomAddr: String = "picpho" + user.id.toString()
                    val intent: Intent = Intent(this, ServerWaitingRoomActivity::class.java)
                    intent.putExtra("roomAddress", roomAddr)
                    intent.putExtra("invitedFriendsJsonArray", invitedFriendsJsonArray.toString())
                    intent.putExtra("isHost", true)
                    intent.putExtra("test", "makeroom")
                    intent.putExtra("roomName", roomName)

                    Log.e("로그", intent.getStringExtra("roomAddress"))
                    Log.d("로그", "makeGroupAction: ${selectedFriendsModelList.size}")
                    mSocket!!.off("kakaoFriendsOnlineReturn")

                    startActivity(intent)
                    finish()
                }
            }
        } else {
            Log.d(TAG, "makeGroupAction: socket null")
        }
    }

    override fun onBackPressed() {
        finish()
    }

    override fun onItemClicked() {
    }

    override fun onDestroy() {
        selectedFriendsModelList.clear()
        selectedFriendsList.clear()
        makeGroupModelList.clear()
        super.onDestroy()
        Log.e(TAG, "onDestroy: MakeGroupActivity 디스트로이", )
    }
}

