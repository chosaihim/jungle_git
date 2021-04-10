package com.example.pic_pho.CellularSocket

import android.util.Log
import com.github.nkzawa.socketio.client.IO.socket
import com.github.nkzawa.socketio.client.Socket
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking
import java.net.URISyntaxException

class SocketUtil {
    companion object {
        private val TAG = "SocketUtil"
        var mSocket: Socket? = null
        fun createAndConnectSocket(): Socket? {
            return try {
//                mSocket = socket("http://52.78.242.130:5000/") //영동
                mSocket = socket("http://3.35.138.31:5000/") //새힘
//                mSocket = socket("http://13.125.236.83:5000/") //정훈
                Log.d(TAG, "createAndConnectSocket: inSocketUtil")
                runBlocking {
                    CoroutineScope(Dispatchers.IO).launch {
                        Log.d(TAG, "createAndConnectSocket: Coroutine launch")
                        mSocket!!.connect()
                    }.join()
                }
                Log.d(TAG, "createAndConnectSocket: success")
                mSocket
            } catch (e: URISyntaxException) {
                Log.d(TAG, "failed")
                null
            }
        }

        fun getSocket() : Socket{
            return mSocket!!
        }
    }
}