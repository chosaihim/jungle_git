package com.example.pic_pho.CellularSocket

import android.util.Log
import com.github.nkzawa.socketio.client.IO
import com.github.nkzawa.socketio.client.IO.socket
import com.github.nkzawa.socketio.client.Socket
import java.net.URISyntaxException
import kotlin.concurrent.thread

class SocketUtill {

    companion object {
        private val TAG = "SocketUtill"
        fun createAndConnetSocket(): Socket? {
            var mSocket: Socket? = null
            try {
//                 mSocket = IO.socket("http://52.78.242.130:5000/") //영동
                mSocket = socket("http://3.35.138.31:5000/") //새힘
                thread() {
                    mSocket.connect()
                }

                return mSocket
            } catch (e: URISyntaxException) {
                Log.d(TAG, "failed")
                return null
            }
        }


    }
}