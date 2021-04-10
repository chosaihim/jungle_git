package com.example.pic_pho.WifiDirect

import android.app.Activity
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.wifi.WpsInfo
import android.net.wifi.p2p.*
import android.os.Bundle
import android.os.StrictMode
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.pic_pho.App
import com.example.pic_pho.LoginActivity
import com.example.pic_pho.R
import com.example.pic_pho.UnCatchTaskService
import com.example.pic_pho.WifiDirect.UI.PeerModel
import com.example.pic_pho.WifiDirect.UI.PeerRecyclerAdapter
import com.example.pic_pho.WifiDirect.UI.PeerViewHolder
import com.example.pic_pho.databinding.ActivityWifiSearchBinding
import com.snatik.storage.Storage
import kotlinx.android.synthetic.main.activity_wifi_search.*
import kotlinx.coroutines.*
import org.jetbrains.anko.toast
import java.lang.Thread.sleep
import java.net.NetworkInterface
import java.util.*
import kotlin.collections.ArrayList

class WifiDirectMainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityWifiSearchBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityWifiSearchBinding.inflate(layoutInflater)
        setContentView(binding.root)

        wifiDirectMainActivity = this
        // 삭제를 위한 storage init
        storage = Storage(applicationContext)

        // 이미 실행되고 있었다면 ? 그룹 삭제
        removeGroup()
        cancelConnect()

        LoginActivity.requestPermissionToUser(this)
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
        LoginActivity.requestPermissionToUser(this) //todo : Wifi 사용 중인지 점검하는 퍼미션 체크 필요

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

        binding.wrapSearchTextview.setOnClickListener {
            searchWifiGroup()
        }
        binding.wrapWifiSearchButtonLayout.setOnClickListener {
            searchWifiGroup()
        }
    }

    private fun searchWifiGroup() {
        discoverPeers(wifiP2pManager!!)
        CoroutineScope(Dispatchers.Main).launch {
            binding.wrapSearchTextview.visibility = View.GONE
            binding.recyclerviewPeerlist.visibility = View.VISIBLE
            binding.wifiMakegroupCardView.isEnabled = false
            binding.wifiMakegroupCardView.visibility = View.GONE
        }
        animateWifiIcon()
    }


    fun animateWifiIcon() {
        CoroutineScope(Dispatchers.Main).launch {
            binding.wifiSearchButton.setImageResource(R.drawable.wifi_one)
            sleep(1000)
            binding.wifiSearchButton.setImageResource(R.drawable.wifi_two)
            sleep(1000)
            binding.wifiSearchButton.setImageResource(R.drawable.wifi_three)
            sleep(1000)
            binding.researchTextview.visibility = View.VISIBLE
        }
    }


    fun createGroupClicked(view: View) {
        CoroutineScope(Dispatchers.IO).launch {
            wifiP2pManager!!.createGroup(channel, object : WifiP2pManager.ActionListener {
                override fun onSuccess() {
                    toast("방이 만들어졌습니다!")
                    isGroupOwner = true
                    var intent: Intent = Intent(App.instance, WaitingForOwnerActivity::class.java)
                    startActivity(intent)
                }

                override fun onFailure(reason: Int) {
                    toast("방 만들기를 실패했습니다\n다시 시도해주세요!")
                }
            })
        }
    }

    override fun onResume() {
        super.onResume()
        Log.d("onResume", "onResume")
        CoroutineScope(Dispatchers.IO).launch {
            // BroadCast Receiver를 등록한다.
            registerReceiver(wifiDirectBroadcastReceiver, intentFilter)
        }
    }


    override fun onPause() {
        super.onPause()
        Log.d(TAG, "onPause")

    }


    override fun onDestroy() {
        Log.d(TAG, "onDestroy")

        runBlocking {
            CoroutineScope(Dispatchers.IO).launch {
                // BroadCast Receiver를 등록해제 한다.
                unregisterReceiver(wifiDirectBroadcastReceiver)
                // Server Thread가 계속 Loop 되는 것을 방지하기 위함. Thread.cancel 활용
                if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
                    WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
                }
                removeGroup()
            }.join()
        }
        super.onDestroy()
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
            CoroutineScope(Dispatchers.IO).launch {
                wifiP2pManager?.connect(channel, config, object : WifiP2pManager.ActionListener {
                    override fun onSuccess() {
                        Log.d(TAG, "onSuccess: ConnectToPeer")
                    }

                    override fun onFailure(reason: Int) {
                        Log.d(TAG, "onFailure: ConnectToPeer")
                    }
                })
            }
        } else {
            Log.d(TAG, "방이 사라졌습니다!")
        }
    }


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

    private fun discoverPeers(wifiP2pManager: WifiP2pManager) {
        CoroutineScope(Dispatchers.IO).launch {
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
        var wifiDirectMainActivity: Activity? = null

        // 삭제를 위한 storage 정의
        var storage: Storage? = null
        var filePathList = ArrayList<String>()


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
            if (wifiP2pManager != null) {
                wifiP2pManager!!.requestGroupInfo(channel) { group ->
                    if (group != null) {
                        wifiP2pManager!!.removeGroup(
                            channel,
                            object : WifiP2pManager.ActionListener {
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

        fun cancelConnect() {
            if (wifiP2pManager != null) {
                wifiP2pManager!!.requestGroupInfo(channel) { group ->
                    if (group != null) {
                        wifiP2pManager!!.cancelConnect(
                            channel,
                            object : WifiP2pManager.ActionListener {
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
}