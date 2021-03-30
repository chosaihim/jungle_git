package com.example.pushtest

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import com.github.nkzawa.socketio.client.IO
import com.github.nkzawa.socketio.client.Socket
import com.google.firebase.iid.FirebaseInstanceId
import kotlinx.android.synthetic.main.activity_main.*
import java.net.URISyntaxException
import kotlin.concurrent.thread


class MainActivity : AppCompatActivity() {

    val TAG: String = "로그"
    lateinit var mSocket: Socket;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


        try {
            mSocket = IO.socket("http://3.35.138.31:5000/")
            thread() {
                mSocket.connect()
            }
        } catch (e: URISyntaxException) {
            Log.d(TAG, "failed")
        }

        button.setOnClickListener {
            mSocket.emit("push_send", 1)

            val token = FirebaseInstanceId.getInstance().token
            Log.e(TAG, "token: ${token}")
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        mSocket.disconnect()
    }

}