package com.example.pic_pho.WifiDirect

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.net.wifi.WpsInfo
import android.net.wifi.p2p.*
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.os.StrictMode
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.PhotoRoom.PhotoRoomActivity
import com.example.pic_pho.R
import com.example.pic_pho.UnCatchTaskService
import com.example.pic_pho.WifiDirect.UI.PeerModel
import com.example.pic_pho.WifiDirect.UI.PeerRecyclerAdapter
import com.example.pic_pho.WifiDirect.UI.PeerViewHolder
import com.example.pic_pho.databinding.ActivityWifiSearchBinding
import kotlinx.android.synthetic.main.activity_wifi_search.*
import kotlinx.coroutines.*
import org.jetbrains.anko.toast
import java.io.File
import java.lang.Thread.sleep
import java.net.NetworkInterface
import java.util.*
import kotlin.collections.ArrayList

class WifiDirectMainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityWifiSearchBinding
    private val handler = Handler(Looper.getMainLooper())

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWifiSearchBinding.inflate(layoutInflater)
        setContentView(binding.root)

        var builder = StrictMode.VmPolicy.Builder()
        StrictMode.setVmPolicy(builder.build())

        // WifiP2PManager 객체 초기화(initailize 함수 호출)
        wifiP2pManager = getSystemService(Context.WIFI_P2P_SERVICE) as WifiP2pManager
        channel = wifiP2pManager?.initialize(this, mainLooper, null)
        wifiDirectBroadcastReceiver = WifiDirectBroadcastReceiver(wifiP2pManager!!, channel!!, this)

        // onCreate 인 경우, Group이 아직 연결되어 있다면 그룹 삭제
        startService(Intent(this, UnCatchTaskService::class.java))

        // 해당 Device Mac 주소 얻음(PhotoInfo 객체에 사용)
        photoOwnerMacAddress = getMacAddr()
        Log.d(TAG, "photoOwnerMacAddress: ${photoOwnerMacAddress}")


        // LoginActivity로 옮깁니다!
        // 앱 실행 시, 권한 묻기 (위치 정보(Wifi-D 사용) 및 스토리지(갤러리) 접근 권한)
//        requestPermissionToUser() //todo : Wifi 사용 중인지 점검하는 퍼미션 체크 필요

        // 리사이클러뷰
        peerRecyclerviewAdapter = PeerRecyclerAdapter()
        (peerRecyclerviewAdapter as PeerRecyclerAdapter).submitList(groupList)
        binding.recyclerviewPeerlist.apply {
            layoutManager =
                LinearLayoutManager(
                    this@WifiDirectMainActivity,
                    LinearLayoutManager.VERTICAL,
                    false
                )
            adapter = peerRecyclerviewAdapter
        }

        // BroadCast Receiver에게 해당 Action들을 Listen하도록 필터링
        intentFilter = IntentFilter().apply {
            addAction(WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION) // 기기에서 Wi-Fi P2P가 활성화되었거나 비활성화되었는지 브로드캐스트합니다.
            addAction(WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION) // discoverPeers()를 호출할 때 브로드캐스트합니다. 일반적으로는 이 인텐트를 애플리케이션에서 처리할 경우, requestPeers()를 호출하여 피어의 업데이트된 목록을 가져올 것입니다.
            addAction(WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION) // 기기의 Wi-Fi 연결 상태가 변경되면 브로드캐스트합니다.
            addAction(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION) // 기기의 상세 정보(예: 기기 이름)가 변경되었는지 브로드캐스트합니다.
            addAction(WifiP2pManager.WIFI_P2P_THIS_DEVICE_CHANGED_ACTION) // 기기의 상세 정보(예: 기기 이름)가 변경되었는지 브로드캐스트합니다.
        }

        // [연결하기] Peer 검색
//        buttonConnect!!.setOnClickListener { discoverPeers(wifiP2pManager!!) }

//        buttonSignal!!.setOnClickListener {
////            var intent = Intent(Intent.ACTION_PICK)
//            var intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
//            intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
//            intent.data = MediaStore.Images.Media.EXTERNAL_CONTENT_URI
//            intent.type = "image/*"
//            startActivityForResult(intent, 100)
//        }
        binding.wrapSearchTextview.setOnClickListener {
            searchWifiGroup()
        }
        binding.wrapWifiSearchButtonLayout.setOnClickListener {
            searchWifiGroup()
        }
    }

    fun searchWifiGroup() {
        discoverPeers(wifiP2pManager!!)
        handler.post {
            kotlin.run {
                binding.wrapSearchTextview.visibility = View.GONE
                binding.recyclerviewPeerlist.visibility = View.VISIBLE
                binding.wifiMakegroupCardView.isEnabled = false
                binding.wifiMakegroupCardView.visibility = View.GONE
            }
        }
        animateWifiIcon()
    }


    fun animateWifiIcon() {
        handler.post {
            kotlin.run {
                binding.wifiSearchButton.setImageResource(R.drawable.wifi_one)
                sleep(1000)
                binding.wifiSearchButton.setImageResource(R.drawable.wifi_two)
                sleep(1000)
                binding.wifiSearchButton.setImageResource(R.drawable.wifi_three)
                sleep(1000)
                binding.researchTextview.visibility = View.VISIBLE
            }
        }
    }


    fun createGroupClicked(view: View) {
        wifiP2pManager!!.createGroup(channel, object : WifiP2pManager.ActionListener {
            override fun onSuccess() {
                toast("Group was created")
            }

            override fun onFailure(reason: Int) {
                toast("Group was removed")
            }
        })
        var intent: Intent = Intent(this, WaitingForOwnerActivity::class.java)
        startActivity(intent)
    }

    override fun onResume() {
        super.onResume()
        Log.d("onResume", "onResume")

        // BroadCast Receiver를 등록한다.
        registerReceiver(wifiDirectBroadcastReceiver, intentFilter)
    }


    override fun onPause() {
        super.onPause()
        Log.d(TAG, "onPause")

    }


    override fun onDestroy() {
        super.onDestroy()
        Log.d(TAG, "onDestroy")


        // BroadCast Receiver를 등록해제 한다.
        unregisterReceiver(wifiDirectBroadcastReceiver)
        // Server Thread가 계속 Loop 되는 것을 방지하기 위함. Thread.cancel 활용
        if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
            WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
        }
        removeGroup()
    }

    //갤러리에서 화면으로 돌아왔을 때, 처리할 부분
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        when (requestCode) {
            100 -> {
                // GroupOwner가 사진 선택하는 부분
                if (data != null) {
                    if (data.clipData != null) {
                        var count = data!!.clipData!!.itemCount // item 선택 개수

                        for (i in 0 until count) {
                            var imageUri = data.clipData!!.getItemAt(i).uri
                            var photoinfo = PhotoInfo(imageUri, photoOwnerMacAddress!!, "picpho")
                            photoInfoList.add(photoinfo)
                            Log.d(TAG, "갤러리에서 눌렀을 때 uri : ${imageUri}")
                        }
                    } else {
                        var imageUri = data.data
                        var photoinfo = PhotoInfo(imageUri!!, photoOwnerMacAddress!!, "picpho")
                        photoInfoList.add(photoinfo)
                        Log.d(TAG, "onActivityResult: 한개만 단일 선택, 다중 선택 아님, ${imageUri}")
                    }
                }

                // 각 Peer들에게 사진 전송 시작
                val intent = Intent(this, SendStreamIntentService::class.java)
                Log.d(TAG, "onCreate: 시그널 접속 ${connectedPeerList.size}")

                for (peer in connectedPeerList) {

                    CoroutineScope(Dispatchers.Default).launch {
                        var counter = 0
                        var clientPhotoCount: Int = connectedPeerMap.get(peer)!!
                        var receivePhotoCount = photoInfoList.size - clientPhotoCount!!
                        var STATUS = 3
                        var uri: Uri?
                        if (isGroupOwner) {
                            Log.d(TAG, "onActivityResult: sendPhoto is Group Owner")
                            if (receivePhotoCount != 0) {
                                Log.d(
                                    TAG,
                                    "onActivityResult: sendPhoto is receivePhotoCount $receivePhotoCount"
                                )
                                // todo : 나 혼자 보냈는데, 아무도 안올림 .. 어캄??/ 밑에 못들어감 ㅅㅂ
                                for (photo in photoInfoList) {
                                    Log.d(TAG, "onActivityResult: sendPhoto is photo $photo")
                                    if (!peer.equals(photo.photoOwnerIP)) {
                                        if (photo.photoOwnerIP.equals("picpho")) {
                                            uri = photo.photoUri
                                        } else {
                                            uri = Uri.fromFile(File(photo.photoUri.toString()))
                                        }
                                        counter++
                                        STATUS -= (counter / receivePhotoCount)
                                        Log.d(TAG, "IsStatus == 2? : ${STATUS}")
                                        intent.putExtra("protocol", "2")
                                        intent.putExtra("photoOwnerMac", photo.photoOwnerMac)
                                        intent.putExtra("serverIP", peer)
                                        intent.putExtra("uri", uri.toString())
                                        intent.putExtra("serverPort", 8989)
                                        intent.putExtra("status", STATUS)
                                        intent.setAction("com.example.picpho.CONNECT_TO_SERVER")
                                        startService(intent)
                                    }
                                }
                            } else {
                                Log.d(TAG, "onActivityResult: Protocol 3 전송")
                                intent.putExtra("protocol", "3")
                                intent.putExtra("serverIP", peer)
                                intent.putExtra("serverPort", 8989)
                                intent.setAction("com.example.picpho.FIRST_CONNECT")
                                startService(intent)
                            }
                        }
                    }
                }

                var intentToPhotoRoom = Intent(this, PhotoRoomActivity::class.java)
                startActivity(intentToPhotoRoom)
            }
        }
    }

    // 피어 연결 (리스트에 나와있는 Peer를 눌렀을 경우, 해당 Peer에게 연결 요청이 가게 된다)
    fun connectToPeer(peerDeviceMAC: String) {
        if (availablePeerList.isNotEmpty()) {
            // 연결할 Peer에 대한 추가적인 정보
            val config = WifiP2pConfig().apply {
                deviceAddress = peerDeviceMAC
                groupOwnerIntent =
                    0 // 해당 Peer가 Client가 되도록 우선순위 할당 (15를 줬을 경우에는, Connect 자체가 이뤄지지 않음.... 왜지...)
                wps.setup =
                    WpsInfo.PBC // 이 내용은 잘 모르겠음.. wps = Wi-Fi Protected Setup임 -> 알아볼 것
            }
            // 지정한 Peer에게 연결 요청을 보냄
            wifiP2pManager?.connect(channel, config, object : WifiP2pManager.ActionListener {
                override fun onSuccess() {
                    Log.d(TAG, "onSuccess: ConnectToPeer")
                }

                override fun onFailure(reason: Int) {
                    Log.d(TAG, "onFailure: ConnectToPeer")
                }
            })
        } else {
            Log.d(TAG, "connectToPeer: availablePeerList is empty")
        }
    }


    // LoginActivity로 옮깁니다!
    // 권한 요청 부분(우리는 갤러리를 위한 WRITE / READ, WiFi - D를 위한 LOCATION, INTERNET이 필요함) -> 권한 부분도 구멍이 많아서 처리해줘야함!!!
//    private fun requestPermissionToUser() {
//        var writePermission =
//            ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
//        var readPermission =
//            ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE)
//        var locationPermission =
//            ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)
//
//        if (writePermission == PackageManager.PERMISSION_DENIED || readPermission == PackageManager.PERMISSION_DENIED || locationPermission == PackageManager.PERMISSION_DENIED) {
//            ActivityCompat.requestPermissions(
//                this,
//                arrayOf(
//                    Manifest.permission.WRITE_EXTERNAL_STORAGE,
//                    Manifest.permission.READ_EXTERNAL_STORAGE,
//                    Manifest.permission.ACCESS_FINE_LOCATION
//                ),
//                1
//            )
//        }
//    }

    // 해당 Device의 Mac Address를 구하는 함수
    fun getMacAddr(): String {
        try {
            val all = Collections.list(NetworkInterface.getNetworkInterfaces())
            for (nif in all) {
                if (!nif.getName().equals("wlan0", ignoreCase = true)) continue

                val macBytes = nif.getHardwareAddress() ?: return ""

                val res1 = StringBuilder()
                for (b in macBytes) {
                    res1.append(String.format("%02X:", b))
                }
                if (res1.length > 0) {
                    res1.deleteCharAt(res1.length - 1)
                }
                return res1.toString()
            }
        } catch (ex: Exception) {
        }

        return "02:00:00:00:00:00"
    }

    fun checkGroupInfo(wifiP2pManager: WifiP2pManager) {
        wifiP2pManager!!.requestGroupInfo(channel) { group ->
            if (group != null) {
                groupList.clear()
                for (peer in group.clientList) {
                    var peerModel =
                        PeerModel(peer.deviceName, peer.deviceAddress, peer.isGroupOwner.toString())
                    groupList.add(peerModel)
                    peerRecyclerviewAdapter!!.notifyDataSetChanged()
                }
                Log.d("group_Info : ", group!!.clientList.toString())
                Log.d(TAG, "button_checkGroup 연결 중인 Peer 수 : ${connectedPeerList.size} ")
            }
        }
    }

    fun cancelConnect(wifiP2pManager: WifiP2pManager) {
        wifiP2pManager!!.cancelConnect(channel, object : WifiP2pManager.ActionListener {
            override fun onSuccess() {
                Log.d(TAG, "onSuccess: Connect Cancel")
            }

            override fun onFailure(reason: Int) {
                Log.d(TAG, "onSuccess: Connect Failed")
            }
        })
    }

    fun discoverPeers(wifiP2pManager: WifiP2pManager) {
        wifiP2pManager?.discoverPeers(channel, object : WifiP2pManager.ActionListener {
            override fun onSuccess() {
                toast("주변에 연결가능한 기기를 찾고 있습니다.\n잠시만 기다려주세요:)")
            }

            override fun onFailure(reason: Int) {
                toast(
                    "주변에 연결가능한 기기를 찾지 못했습니다.\n" +
                            "다시 시도해 주세요!:)"
                )
            }
        })
    }

    companion object {
        var photoOwnerMacAddress: String? = null
        var groupMemberCount: Int = 0
        var sentPhotoCount: Int = 0
        var isGroupOwner = false
        var groupOwnerIP: String? = null // IP
        var photoInfoList = ArrayList<PhotoInfo>()
        var groupList = ArrayList<PeerModel>()
        val availablePeerList = ArrayList<WifiP2pDevice>()
        val connectedPeerList = ArrayList<String>()
        val connectedPeerMap = mutableMapOf<String, Int>()
        var wifiP2pManager: WifiP2pManager? = null
        var channel: WifiP2pManager.Channel? = null
        var peerRecyclerviewAdapter: RecyclerView.Adapter<PeerViewHolder>? = null
        var wifiDirectBroadcastReceiver: BroadcastReceiver? = null


        var uiHandler = Handler()
        private lateinit var intentFilter: IntentFilter

        private const val TAG = "WifiDirectMainActivity"

        // Photo 전송, IntentService로 보내진다.
        fun sendToServerPhotos(context: Context) {

            // 그룹 오너가 있고, 해당 디바이스가 Peer인 경우에 전송 시작
            if (groupOwnerIP != null && !isGroupOwner && !photoInfoList.isEmpty()) {

                val intent = Intent(context, SendStreamIntentService::class.java)

                var photoCountDigit = (photoInfoList.size).toString().length

                Log.d(TAG, "sendToServerPhotos 자리 수 세기 :  ${photoCountDigit}")
                var i = 1
                for (photo in photoInfoList) {
                    if (!isGroupOwner) {
                        intent.putExtra("protocol", "2")
                        intent.putExtra("photoOwnerMac", photo.photoOwnerMac)
                        intent.putExtra("serverIP", groupOwnerIP)
                        intent.putExtra("serverPort", 8989)
                        intent.putExtra("uri", photo.photoUri.toString())
                        intent.putExtra("status", Integer(i / photoInfoList.size))
                        intent.putExtra("clientPhotoDigit", photoCountDigit)
                        intent.putExtra("clientPhotoCount", photoInfoList.size)
                        intent.setAction("com.example.picpho.CONNECT_TO_SERVER")
                        context.startService(intent)
                        i++
                    }
                }
            }
            sentPhotoCount++ // count로 전송 완료임을 나타낼 수 있나..?
        }

        fun removeGroup() {
            wifiP2pManager!!.requestGroupInfo(channel) { group ->
                if (group != null) {
                    wifiP2pManager!!.removeGroup(channel, object : WifiP2pManager.ActionListener {
                        override fun onSuccess() {
                            Log.d(TAG, "onSuccess: 그룹 삭제")
                            isGroupOwner = false;
                        }

                        override fun onFailure(reason: Int) {
                            Log.d(TAG, "onFailure: 그룹 삭제 실패")
                        }
                    })
                }
            }
        }
    }
}