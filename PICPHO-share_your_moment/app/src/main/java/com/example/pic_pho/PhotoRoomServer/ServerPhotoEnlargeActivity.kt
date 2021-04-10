package com.example.pic_pho.PhotoRoomServer

import android.os.Bundle
import android.util.Log
import androidx.appcompat.app.AppCompatActivity
import androidx.core.net.toUri
import com.davemorrissey.labs.subscaleview.ImageSource
import com.davemorrissey.labs.subscaleview.SubsamplingScaleImageView
import com.example.pic_pho.App
import com.example.pic_pho.ImageHandler.ImageHandler.Companion.getFullPathFromUri
import com.example.pic_pho.ImageHandler.ImageHandler.Companion.getOrientationOfImage
import com.example.pic_pho.databinding.ActivityEnlargePhotoBinding
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch


class ServerPhotoEnlargeActivity : AppCompatActivity() {

    private lateinit var binding: ActivityEnlargePhotoBinding


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityEnlargePhotoBinding.inflate(layoutInflater)
        setContentView(binding.root)


        var intent = intent

        binding.imageViewQuitEnlargePhoto.setOnClickListener {
            finish()
        }

        var imagepath = intent.getStringExtra("uri")
        var orientation = intent.getIntExtra("orientation",-200)

        Log.d("TAG", "onCreate:수정했다2!${orientation}")
        CoroutineScope(Dispatchers.Main).launch {
            if (orientation != -1) {
                binding.imageViewEnlargePhoto.orientation =
                    SubsamplingScaleImageView.ORIENTATION_USE_EXIF
            } else {
                binding.imageViewEnlargePhoto.orientation =
                    SubsamplingScaleImageView.ORIENTATION_90
            }

            binding.imageViewEnlargePhoto.setImage(ImageSource.uri(imagepath.toUri()))
        }
    }

    override fun onBackPressed() {
        super.onBackPressed()
        finish()
    }
}