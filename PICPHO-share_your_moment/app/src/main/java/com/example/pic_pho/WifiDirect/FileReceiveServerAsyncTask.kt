package com.example.pic_pho.WifiDirect

import android.annotation.SuppressLint
import android.content.ContentValues.TAG
import android.content.Context
import android.os.AsyncTask
import android.util.Log
import java.io.IOException
import java.net.ServerSocket
import java.net.Socket

// serverSocket을 열고 accept함으로서 connect를 기다린다. 이후에 FileReceiveActionThread를 실행해준다.
class FileReceiveServerAsyncTask(
    private val context: Context
) : AsyncTask<Void, Void, String?>() {

    @SuppressLint("RestrictedApi")
    override fun doInBackground(vararg params: Void): String? {

        Log.d("ServerSide", "doInBackground Start")
        try {
            val serverSocket = ServerSocket(8989)
            serverSocket.reuseAddress
            var client : Socket
//            var file : File? = null

            while(true) {
                if(this.isCancelled){
                    Log.d("ServerSide", "doInBackground Canceled")
                    WifiDirectBroadcastReceiver.ServerThread = null
                    break
                }

                try{
                    client = serverSocket.accept()
                    Log.d(TAG, "doInBackground: filereceiveAction thread 시작하기 바로 전!")
                    FileReceiveActionThread(client = client, context = context).run()

                }catch(e : IOException){
                    Log.d(TAG, "doInBackground: FileReceiverServerAsyncTask : accept 실패 후 while문 break")
                    break
                }
            }

            serverSocket.close()

            Log.d("ServerSide", "doInBackground Finished")
            return null

        } catch (e: IOException) {
            e.printStackTrace()
            Log.d("dointbackground", e.toString())
            return null
        }
    }
}