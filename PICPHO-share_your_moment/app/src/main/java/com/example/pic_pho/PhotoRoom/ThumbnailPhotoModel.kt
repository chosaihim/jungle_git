package com.example.pic_pho.PhotoRoom

import android.net.Uri

class ThumbnailPhotoModel(
    var thumbnailPhoto: Uri?  = null,
    var isPicked : Boolean = false,
    var path : String? = null
)