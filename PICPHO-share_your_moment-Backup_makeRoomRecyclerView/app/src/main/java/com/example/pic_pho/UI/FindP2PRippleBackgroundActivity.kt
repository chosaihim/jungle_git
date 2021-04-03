package com.example.pic_pho.UI

import android.os.Bundle
import android.view.View
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import com.example.pic_pho.R
import com.example.pic_pho.databinding.ActivityFindP2PRippleBackgroundBinding
import com.skyfishjy.library.RippleBackground


class FindP2PRippleBackgroundActivity : AppCompatActivity() {

    private lateinit var binding: ActivityFindP2PRippleBackgroundBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFindP2PRippleBackgroundBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val rippleBackground = findViewById<View>(R.id.content) as RippleBackground
        val imageView: ImageView = findViewById<View>(R.id.centerImage) as ImageView
        imageView.setOnClickListener { rippleBackground.startRippleAnimation() }
    }
}