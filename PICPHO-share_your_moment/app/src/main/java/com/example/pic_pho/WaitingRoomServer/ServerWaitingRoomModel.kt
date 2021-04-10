package com.example.pic_pho.WaitingRoomServer

import com.google.gson.JsonElement

data class ServerWaitingRoomModel(
//    var userId: JsonElement? = null,
//    var name: JsonElement? = null,
//    var profileImage: JsonElement? = null
    var userId: Int = 0,
    var name: String? = null,
    var profileImage: String? = null,
    var status:Int=0
//0 사진 선택 전 회색구름
//1 사진 선택 완료 파란구름
//2 전송/수신완료 파란 화살표 구름
)

