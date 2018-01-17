package uk.ac.cam.cl.loclogger;

//import android.hardware.SensorManager;

public class ApplicationConstants {
    public static final boolean DEBUG = true;
    public static final String KEY_UUID = "uuid";
    public static final String ACCOUNT_TYPE = "loclogger.cl.cam.ac.uk";
    public static final int LOCATION_PERMISSIONS_CODE = 17;
    public static final String TAG = "LocationLogger";


    // LOGGING
    // Measure location every x seconds
    public static final int LOG_INTERVAL_SECONDS = 30;
    public static final long LOG_INTERVAL_MS = LOG_INTERVAL_SECONDS * 1000;
    // Locations less accurate than this are not recorded
    public static final int MIN_ACCURACY_METRES = 30;
    public static final long ACTIVITY_INTERVAL_MS = 10000;
    // We need to be this % sure that the user is moving to log a location
    public static final int ACTIVITY_MOVING_CONFIDENCE = 50;

    public static final int ACC_LOG_INTERVAL_SECONDS = 30;
    //public static final long ACC_LOG_INTERVAL_MS = ACC_LOG_INTERVAL_SECONDS * 1000;

    // For JSON
    public static final String DEVICE_MODEL = "deviceModel";
    public static final String DEVICE_OPSYS = "deviceOpSys";
    public static final String STUDY_ID = "studyID";
    public static final String TIMESTAMP = "timestamp";
    public static final String TIME = "time";
    public static final String OFFSET = "offset";
    public static final String LOCATION = "location";
    public static final String LOCATION_LATITUDE = "latitude";
    public static final String LOCATION_LONGITUDE = "longitude";
    public static final String ANDROID = "Android";
    /*public static final String ACCELERATION = "accelerometer";
    public static final String ACCELERATION_X = "xAxis";
    public static final String ACCELERATION_Y = "yAxis";
    public static final String ACCELERATION_Z = "zAxis";

    public static final int ACC_SAMPLING_DELAY  = SensorManager.SENSOR_DELAY_GAME;
    public static final float ACC_LOW_PASS_ALPHA = 0.25f;
    public static final long ACC_SAMPLING_WINDOW_MILLIS = 10000L;
    */

    public static final long LOCATION_INTERVAL = 20*1000;
    public static final long LOCATION_FASTEST_INTERVAL = 20*1000;

    // UPLOAD
    public static final String KEY_UPLOAD_TIME = "lastUploadTime";
    // Upload every x minutes, if the phone is connected to WiFi.
    private static final long UPLOAD_INTERVAL_MINUTES = 6L * 60L;  // 24L * 60L; //5L; // 1; //every 12 hours;
    public static final long UPLOAD_INTERVAL_SECONDS = 60L * UPLOAD_INTERVAL_MINUTES;
    public static final long UPLOAD_INTERVAL_MILLIS = 1000L * 60L * UPLOAD_INTERVAL_MINUTES;


    // GRAPH CONSTRUCTION (not used, but see TestGraphUtils.java
    // Dwell time required to consider a collection of points a node
    private static final int NEW_LOCATION_TIME_THRESHOLD_MINUTES = 5;
    public static final long NEW_LOCATION_TIME_THRESHOLD_MS =
            1000 * 60 * NEW_LOCATION_TIME_THRESHOLD_MINUTES;
    // Distance outside which a user is considered to have left a node
    public static final int NEW_LOCATION_DISTANCE_THRESHOLD_METRES = 200;


    // ******** NEW CODE *******//
    public static final String PASSWD = "password";
    //public static final String EMAIL = "email";

    // AUTHENTICATION
    /* CONSTANTS FOR THE AUTHORIZATION PROCESS */
    public static final String CLIENT_ID = "IfmtmKZTFkiBUR3zHOF4tdJDyeo40xNQ1MN2PRmD";
    public static final String CLIENT_SECRET = "A0HsxlF8KdZvfCWPWabvPHpPg59wjLD1Ko79kedCU75WCR3LBQ94k75xHrmvvWZNHAkYoaPMR0Rlx6PdB5cE8By93IedM31trQvZEDXmiuIUB3AY5NqDPU5VbjTVpXW9";

    //These are constants used for build the urls
    public static final String AUTHORIZATION_URL = "https://pizza.cl.cam.ac.uk/camtrac/api/create_app_user_preauth//";
    public static final String ACCESS_TOKEN_URL = "https://pizza.cl.cam.ac.uk/camtrac/auth/token/";
    public static final String GRANT_TYPE = "password";//"refresh_token";

    public static final String SERVER_URL = "https://pizza.cl.cam.ac.uk/camtrac/api/receive/"; //"http://pizza.cl.cam.ac.uk/dm754/receive.php";

    public static final String ACCESS_TOKEN = "access_token";
    public static final String REFRESH_TOKEN = "refresh_token";

    public static final String APP_PASSWORD = "cam_rocks_hard_!@#$";
    public static final String APP_EMAIL = "mobsys@cam.ac.uk";

    // ********* END NEW CODE ***//
}
