package com.example.pushtest;

public class FirebaseMessagingService extends com.google.firebase.messaging.FirebaseMessagingService {
//
//    private static final String TAG = "로그"; // "FirebaseMsgService";
//
//    private String msg, title;
//
//
//    @Override
//    public void onMessageReceived(RemoteMessage remoteMessage) {
//
//        // TODO(developer): Handle FCM messages here.
//        // Not getting messages here? See why this may be: https://goo.gl/39bRNJ
//        Log.e(TAG, "onMessageReceived");
//
//        title = remoteMessage.getNotification().getTitle();
//        msg   = remoteMessage.getNotification().getBody();
//
//
//        Intent intent = new Intent(this, MainActivity.class);
//        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
//
//        //notification 발생했을 때 해주는 행위를 정의
//        PendingIntent contentIntent = PendingIntent.getActivity(this,0,new Intent(this, MainActivity.class),0);
//
//        NotificationCompat.Builder mBuilder = new NotificationCompat.Builder(this).setSmallIcon(R.mipmap.ic_launcher)
//                .setContentTitle(title)
//                .setContentText(msg)
//                .setAutoCancel(true)
//                .setSound(RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION))
//                .setVibrate(new long[]{1, 1000});
//
//        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
//
//        notificationManager.notify(0, mBuilder.build());
//
//        mBuilder.setContentIntent(contentIntent);
//

//    }
}
