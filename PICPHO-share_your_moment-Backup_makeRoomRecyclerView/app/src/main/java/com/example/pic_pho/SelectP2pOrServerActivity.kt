package com.example.pic_pho

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import com.example.pic_pho.Lobby.LobbyActivity
import com.example.pic_pho.WifiDirect.WifiDirectMainActivity
import com.example.pic_pho.databinding.ActivitySelectP2pOrServerBinding
import com.kakao.sdk.user.UserApiClient


class SelectP2pOrServerActivity : AppCompatActivity() {
    private var TAG = "SelectP2pOrServerActivi"
    private lateinit var binding: ActivitySelectP2pOrServerBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySelectP2pOrServerBinding.inflate(layoutInflater)
        setContentView(binding.root)

        UserApiClient.instance.me { user, error ->
            if (error != null) {
                Log.e(TAG, "사용자 정보 요청 실패", error)
            } else if (user != null) {
                var scopes = mutableListOf<String>()
                if (user.kakaoAccount?.emailNeedsAgreement == true) {
                    scopes.add("account_email")
                }
                if (user.kakaoAccount?.birthdayNeedsAgreement == true) {
                    scopes.add("birthday")
                }
                if (user.kakaoAccount?.birthyearNeedsAgreement == true) {
                    scopes.add("birthyear")
                }
                if (user.kakaoAccount?.genderNeedsAgreement == true) {
                    scopes.add("gender")
                }
                if (user.kakaoAccount?.phoneNumberNeedsAgreement == true) {
                    scopes.add("phone_number")
                }
                if (user.kakaoAccount?.profileNeedsAgreement == true) {
                    scopes.add("profile")
                }
                if (user.kakaoAccount?.ageRangeNeedsAgreement == true) {
                    scopes.add("age_range")
                }
                if (user.kakaoAccount?.ciNeedsAgreement == true) {
                    scopes.add("account_ci")
                }

                if (scopes.count() > 0) {
                    Log.d(TAG, "사용자에게 추가 동의를 받아야 합니다.")

                    UserApiClient.instance.loginWithNewScopes(this, scopes) { token, error ->
                        if (error != null) {
                            Log.e(TAG, "사용자 추가 동의 실패", error)
                        } else {
                            Log.d(TAG, "allowed scopes: ${token!!.scopes}")

                            // 사용자 정보 재요청
                            UserApiClient.instance.me { user, error ->
                                if (error != null) {
                                    Log.e(TAG, "사용자 정보 요청 실패", error)
                                } else if (user != null) {
                                    Log.i(TAG, "사용자 정보 요청 성공")
                                }
                            }
                        }
                    }
                }



                Log.i(
                    TAG, "사용자 정보 요청 성공" +
                            "\n회원번호: ${user.id}" +
                            "\n닉네임: ${user.kakaoAccount?.profile?.nickname}" +
                            "\n프로필사진: ${user.kakaoAccount?.profile?.thumbnailImageUrl}"
                )
            }
        }

        // true = invisible , false = visible
        var nearbyQuestionMarkVisibility = true
        binding.nearbyQuestionMark.setOnClickListener {
            if (nearbyQuestionMarkVisibility) {
                binding.nearbyHelpImage.visibility = View.VISIBLE
                nearbyQuestionMarkVisibility = false
            } else {
                binding.nearbyHelpImage.visibility = View.INVISIBLE
                nearbyQuestionMarkVisibility = true
            }
        }
        var farQuestionMarkVisibility = true
        binding.farQuestionMark.setOnClickListener {
            if (farQuestionMarkVisibility) {
                binding.farHelpImage.visibility = View.VISIBLE
                farQuestionMarkVisibility = false
            } else {
                binding.farHelpImage.visibility = View.INVISIBLE
                farQuestionMarkVisibility = true

            }
        }
    }

    fun selectP2pMode(view: View) {
        val intent = Intent(this, WifiDirectMainActivity::class.java)
        startActivity(intent)
    }

    fun selectServerMode(view: View) {
        val intent = Intent(this, LobbyActivity::class.java)
        startActivity(intent)
    }
}