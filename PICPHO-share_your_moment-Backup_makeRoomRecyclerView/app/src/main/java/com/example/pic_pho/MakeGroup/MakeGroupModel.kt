package com.example.pic_pho.MakeGroup

data class MakeGroupModel(
    var isSelected: Boolean? = false,
    var userId:Int = 0,
    var name: String? = null,
    var profileImage: String? = null
)