package com.example.pic_pho.WifiDirect

import android.Manifest
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.net.wifi.p2p.WifiP2pManager
import android.os.AsyncTask
import android.util.Log
import android.widget.Toast
import androidx.core.app.ActivityCompat
import com.example.pic_pho.WifiDirect.UI.PeerModel


// WifiDirect 상태 변화를 감지해주는 class
class WifiDirectBroadcastReceiver(
    private val manager: WifiP2pManager,
    private val channel: WifiP2pManager.Channel,
    private val mainActivity: WifiDirectMainActivity
) : BroadcastReceiver() {

    companion object {
        var ServerThread: AsyncTask<Void, Void, String?>? = null
    }

    override fun onReceive(context: Context, intent: Intent) {
        // This method is called when the BroadcastReceiver is receiving an Intent broadcast.
        when (intent.action) {

            // WiFi P2P 활성화 시
            WifiP2pManager.WIFI_P2P_STATE_CHANGED_ACTION -> {
                // Determine if Wifi P2P mode is enabled or not, alert
                // the Activity.

                // WiFi 단말의 상태를 가져온 뒤, enable 상태를 점검한다.
                when (intent.getIntExtra(WifiP2pManager.EXTRA_WIFI_STATE, -1)) {
                    WifiP2pManager.WIFI_P2P_STATE_ENABLED -> {
                        // Wifi P2P is enabled
                    }
                    else -> {
                        // Wifi P2P is not enabled
                        Toast.makeText(context, "Wifi를 켜주세요!\n 와이파이존이 아니어도 괜찮아요!", Toast.LENGTH_SHORT).show()
                        //todo : 권한 신청하는 로직 만들기
                    }
                }
            }
            // 연결 가능한 피어 목록이 변경 시 -> requestPeers 구현
            WifiP2pManager.WIFI_P2P_PEERS_CHANGED_ACTION -> {

                // The peer list has changed! We should probably do something about that.
                Toast.makeText(context, "WIFI_P2P_PEERS_CHANGED_ACTION", Toast.LENGTH_SHORT).show()

                if (ActivityCompat.checkSelfPermission(
                        context,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    ) != PackageManager.PERMISSION_GRANTED
                ) {
                    return
                }

                WifiDirectMainActivity.wifiP2pManager!!.requestGroupInfo(
                    WifiDirectMainActivity.channel
                ) { group ->
                    if (group == null) {
                        manager.requestPeers(channel) { peers ->
                            WifiDirectMainActivity.availablePeerList.clear()
                            WifiDirectMainActivity.availablePeerList.addAll(peers!!.deviceList)
                            WifiDirectMainActivity.groupList.clear()
                            for (peer in peers!!.deviceList) {
//                                Toast.makeText(context, "first type is ${peer.primaryDeviceType}, second type is ${peer.secondaryDeviceType}", Toast.LENGTH_LONG).show()
                                var primaryDeviceTypeLastWord = peer.primaryDeviceType.endsWith("5")
                                if(peer.isGroupOwner && !WifiDirectMainActivity.isGroupOwner && primaryDeviceTypeLastWord) {
                                    WifiDirectMainActivity.groupList.add(
                                        PeerModel(
                                            peer.deviceName + "의 방",
                                            peer.deviceAddress,
                                            peer.isGroupOwner.toString()
                                        )
                                    )
                                }
                            }
                            WifiDirectMainActivity.peerRecyclerviewAdapter!!.notifyDataSetChanged()
                        }
                    }else{
                        WifiDirectMainActivity.groupList.clear()
                        WifiDirectMainActivity.peerRecyclerviewAdapter!!.notifyDataSetChanged()
                    }
                    // todo : recycler adapter list에 값 넣고, notify 해줄 것
                }
            }

            // WiFi P2P 연결 상태가 변경되었음을 나타냄 -> requestConnectionInfo() 호출
            WifiP2pManager.WIFI_P2P_CONNECTION_CHANGED_ACTION -> {
                // Connection state changed! We should probably do something about that.

                Toast.makeText(context, "WIFI_P2P_CONNECTION_CHANGED_ACTION", Toast.LENGTH_SHORT)
                    .show()

                manager.requestConnectionInfo(channel) { info ->

                    // GroupOwner Action 정의
                    if (info!!.groupFormed && info.isGroupOwner) {
//                        WifiDirectMainActivity.textViewGroupOwner!!.text = "서버입니다."
                        WifiDirectMainActivity.isGroupOwner = true
//                        WifiDirectMainActivity.buttonConnect!!.visibility = View.GONE
//                        WifiDirectMainActivity.buttonSignal!!.visibility = View.VISIBLE

                        WifiDirectMainActivity.wifiP2pManager!!.requestGroupInfo(
                            WifiDirectMainActivity.channel
                        ) { group ->
                            if (group != null) {
                                Log.d("group_Info : ", group!!.clientList.toString())
                                Log.d("group_Info : ", "group size is ${group!!.clientList.size}")
                                WifiDirectMainActivity.groupMemberCount = group!!.clientList.size

                                WifiDirectMainActivity.groupList.clear()
                                for (peer in group.clientList) {

                                    var peerModel = PeerModel(
                                        peer.deviceName,
                                        peer.deviceAddress,
                                        peer.isGroupOwner.toString()
                                    )
                                    WifiDirectMainActivity.groupList.add(peerModel)
                                    WifiDirectMainActivity.peerRecyclerviewAdapter!!.notifyDataSetChanged()
                                    if (WaitingForOwnerActivity.wifiWaitingRecyclerAdapter != null)
                                        WaitingForOwnerActivity.wifiWaitingRecyclerAdapter!!.notifyDataSetChanged()
                                }
                            }
                        }
                        if (ServerThread == null) {
                            ServerThread = FileReceiveServerAsyncTask(context).execute()
                        }
                    
                    // Peer Action 정의
                    } else if (info!!.groupFormed) {
//                        WifiDirectMainActivity.textViewGroupOwner!!.text = "클라이언트 입니다"
                        WifiDirectMainActivity.isGroupOwner = false
                        WifiDirectMainActivity.groupOwnerIP = info.groupOwnerAddress.hostAddress
                        
                        // 클라이언트도 본인의 서버 소켓을 연다
                        if (ServerThread == null) {
                            // GroupOwner에게 인사함. 소켓 통신을 시도
                            if (WifiDirectMainActivity.groupOwnerIP != null && !WifiDirectMainActivity.isGroupOwner) {
                                val intent = Intent(context, SendStreamIntentService::class.java)
                                intent.putExtra("protocol", "1")
                                intent.putExtra("serverIP", WifiDirectMainActivity.groupOwnerIP)
                                intent.putExtra("serverPort", 8989)
                                intent.setAction("com.example.picpho.FIRST_CONNECT")
                                context.startService(intent)
                            }
                            ServerThread = FileReceiveServerAsyncTask(context).execute()
                        }
                        var intent = Intent(context, WaitingForOwnerActivity::class.java)
                        context.startActivity(intent)
                    }
                }
            }
        }
    }
}
