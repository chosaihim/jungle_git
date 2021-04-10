package com.example.pic_pho

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import com.example.pic_pho.WifiDirect.WifiDirectBroadcastReceiver
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity

class UnCatchTaskService() : Service() {
    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    override fun onTaskRemoved(rootIntent: Intent?) {
        super.onTaskRemoved(rootIntent)
        Log.e("Error", "onTaskRemoved - " + rootIntent)
        WifiDirectMainActivity.removeGroup()
        if (WifiDirectBroadcastReceiver.ServerThread != null && !WifiDirectBroadcastReceiver.ServerThread!!.isCancelled) {
            WifiDirectBroadcastReceiver.ServerThread!!.cancel(false)
        }
        // todo : 핸들링 할 부분
        stopSelf()

    }
}