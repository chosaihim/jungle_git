package com.example.pic_pho.Lobby

import android.util.Log
import com.example.pic_pho.PhotoRoomServer.Drawer.ServerDrawerMemberModel

class GroupModel(
    var groupName: String,
    var presentImage: String,
    var eventDate: String,
    var absolutePathList: String,
    var memberUidList: String
)