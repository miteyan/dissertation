package uk.ac.cam.cl.loclogger.location;

import android.Manifest;
import android.app.PendingIntent;
//import android.content.Context;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
//import android.hardware.Sensor;
//import android.hardware.SensorEvent;
//import android.hardware.SensorEventListener;
//import android.hardware.SensorManager;
import android.location.Location;
import android.os.Bundle;
//import android.os.Handler;
//import android.os.CountDownTimer;
import android.os.IBinder;
import android.support.v4.app.ActivityCompat;
import android.util.Log;
import android.widget.Toast;

import com.commonsware.cwac.wakeful.WakefulIntentService;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.ActivityRecognition;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

//import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;
import java.util.Calendar;

//import java.util.ArrayList;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.activity.ActivityRecognitionService;
import uk.ac.cam.cl.loclogger.alarms.ServiceAlarm;
//import uk.ac.cam.cl.locationlogger.logging.AccelerationLogger;
import uk.ac.cam.cl.loclogger.logging.FileLogger;
import uk.ac.cam.cl.loclogger.logging.LocationLogger;

/*public class LocationTrackerService extends WakefulIntentService implements
        GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener,
        LocationListener, SensorEventListener { */
public class LocationTrackerService extends WakefulIntentService implements
            GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener,
            LocationListener {

    // location
    private final LocationRequest mLocationRequest;
    private GoogleApiClient mGoogleApiClient;
    public static boolean userActivity = true;

    // acceleration
    /*private ArrayList<Float> xAxis, yAxis, zAxis;
    private ArrayList<Long> timestamps;
    private SensorManager sensorManager = null;
    private Sensor sensor = null;*/

    public LocationTrackerService() {
        super(ApplicationConstants.TAG);
        mLocationRequest =
                LocationRequest.create().setPriority(LocationRequest.PRIORITY_HIGH_ACCURACY)
                        .setInterval(ApplicationConstants.LOCATION_INTERVAL).setFastestInterval(ApplicationConstants.LOCATION_FASTEST_INTERVAL);
    }

    @Override public IBinder onBind(Intent intent) {
        return null;
    }

    @Override protected void doWakefulWork(Intent intent) {

        //if (intent.getExtras().hasFileDescriptors()) {
            // FOR LOCATION
            FileLogger.log("Work received.", this.getApplicationContext());
            // Set alarm for next time.
            ServiceAlarm alarm = new ServiceAlarm();
            scheduleAlarms(alarm, this.getApplicationContext());
            mGoogleApiClient = new GoogleApiClient.Builder(LocationTrackerService.this)
                    .addApi(ActivityRecognition.API).addApi(LocationServices.API)
                    .addConnectionCallbacks(LocationTrackerService.this)
                    .addOnConnectionFailedListener(LocationTrackerService.this).build();
            FileLogger.log("Making connection request.", this.getApplicationContext());
            mGoogleApiClient.blockingConnect();

        //}else {

            // FOR ACCELERATION
            /* FileLogger.log("Work received (acc).", this.getApplicationContext());

            // Set alarm for next time.
            //ServiceAlarm alarmAcc = new ServiceAlarm();
            //scheduleAlarms(alarmAcc, this.getApplicationContext());

            xAxis = new ArrayList<Float>();
            yAxis = new ArrayList<Float>();
            zAxis = new ArrayList<Float>();
            timestamps = new ArrayList<Long>();

            sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
            sensor = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
            sensorManager.registerListener(this, sensor,
                    ApplicationConstants.ACC_SAMPLING_DELAY);
            FileLogger.log("Start to listen to acc.", this.getApplicationContext());

            // stop the sensor and service after window milliseconds
            final SensorEventListener listener = this;
            final Context context = this.getApplicationContext();

            new Handler(getMainLooper()).postDelayed(new Runnable() {
                @Override
                public void run() {
                    sensorManager.unregisterListener(listener);
                    stopSelf();
                    FileLogger.log("Stop listening to acc.", context);
                    // log acc data
                    try {
                        AccelerationLogger.log(buildStringToLog(), context);
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            }, ApplicationConstants.ACC_SAMPLING_WINDOW_MILLIS);
            Until here commented for removing acceleration */

        /*new CountDownTimer(ApplicationConstants.ACC_SAMPLING_WINDOW_MILLIS, 1000) {
            public void onTick(long millisUntilFinished) {
                FileLogger.log("seconds remaining: " + millisUntilFinished / 1000, context);
            }

            public void onFinish() {
                sensorManager.unregisterListener(listener);
                stopSelf();
                FileLogger.log("Stop listening to acc.", context);
                // log acc data
                try {
                    AccelerationLogger.log(buildStringToLog(), context);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }.start();*/
        //}
    }

    public void handleNewLocation(Location location) throws JSONException {
        FileLogger.log("Removing location updates.", this.getApplicationContext());
        LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
        FileLogger.log("Handling new location.", this.getApplicationContext());
        LocationLogger.log(buildStringToLog(location), this.getApplicationContext());
    }

    private String buildStringToLog(Location loc) throws JSONException {
        JSONObject json = new JSONObject();
        //json.put(ApplicationConstants.DEVICE_MODEL, ApplicationConstants.ANDROID);
        //json.put(ApplicationConstants.TIMESTAMP, loc.getTime());
        //json.put(ApplicationConstants.DEVICE_OPSYS, Build.VERSION.RELEASE);
        JSONObject timestamp = new JSONObject();
        timestamp.put(ApplicationConstants.TIME, loc.getTime());
        timestamp.put(ApplicationConstants.OFFSET, getOffset());
        json.put(ApplicationConstants.TIMESTAMP, timestamp);
        JSONObject location = new JSONObject();
        location.put(ApplicationConstants.LOCATION_LATITUDE, loc.getLatitude());
        location.put(ApplicationConstants.LOCATION_LONGITUDE, loc.getLongitude());
        json.put(ApplicationConstants.LOCATION, location);
        Log.d("MYINFO", "Location stored: "+ json.toString());
        return json.toString() + "\n";
    }

    @Override public void onConnected(Bundle bundle) {
        Intent intent = new Intent(this, ActivityRecognitionService.class);
        PendingIntent pendingIntent =
                PendingIntent.getService(this, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);
        ActivityRecognition.ActivityRecognitionApi
                .requestActivityUpdates(mGoogleApiClient, ApplicationConstants.ACTIVITY_INTERVAL_MS,
                        pendingIntent);

        FileLogger.log("Services connected.", this.getApplicationContext());

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED && ActivityCompat
                .checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED) {
            return;
        }
//        Log.d("MYINFO",LocationTrackerActivity.getUserID(getApplicationContext()));
        // Don't get a location if the user is still.
//        if (!userActivity) {
//            FileLogger.log("User is still. Do not get location.", getApplicationContext());
//            //LocationLogger.log("FORCED UPLOAD CHECK", this.getApplicationContext());
//            return;
//        }

        FileLogger.log("Getting location.", this.getApplicationContext());
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);

        if (location == null)
        {
            FileLogger.log("Location null ", this.getApplicationContext());
            return;
        }


//        fileName = year_weekno.csv
//        format
//        2009-11-10 20:26:54,46.52,6.629
        //save location to file
        //edited
        Context context = getApplicationContext();
        CharSequence text = location.getLatitude() + " " + location.getLongitude();
        int duration = Toast.LENGTH_SHORT;
        Toast toast = Toast.makeText(context, text, duration);
        toast.show();

        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.UK);
        Date now = new Date();
        String strDate = sdfDate.format(now);
        String row = strDate + "," + location.getLatitude() + "," + location.getLongitude() + "\n";


//        Toast.makeText(context, weekNo, Toast.LENGTH_LONG).show();
//        String fileName = calendar.get(Calendar.YEAR) + "_" + calendar.get(Calendar.WEEK_OF_YEAR)+ ".csv";
        String fileName = "2018_3.csv";
        writeToFile(fileName, row, context);


        String x = readFromFile(fileName, context);
        System.out.println(x);
        System.out.println(x.split(System.getProperty("line.separator")).length);


        if (location.getAccuracy() > ApplicationConstants.MIN_ACCURACY_METRES ||
                System.currentTimeMillis() - location.getTime() >
                        ApplicationConstants.LOG_INTERVAL_MS) {
            FileLogger.log("Location inaccurate/old (accuracy " + location.getAccuracy() + ") " +
                    location, this.getApplicationContext());
            mLocationRequest.setExpirationDuration(ApplicationConstants.LOG_INTERVAL_MS);
            LocationServices.FusedLocationApi
                    .requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
            //LocationLogger.log("FORCED UPLOAD CHECK", this.getApplicationContext());
        }

        else {
            try {
                FileLogger.log("Suitable location.", this.getApplicationContext());
                handleNewLocation(location);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }
    }

    private String readFromFile(String fileName, Context context) {
        String ret = "";
        try {
            InputStream inputStream = context.openFileInput(fileName);
            if ( inputStream != null ) {
                InputStreamReader inputStreamReader = new InputStreamReader(inputStream);
                BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
                String receiveString = "";
                StringBuilder stringBuilder = new StringBuilder();

                while ( (receiveString = bufferedReader.readLine()) != null ) {
                    stringBuilder.append(receiveString);
                }

                inputStream.close();
                ret = stringBuilder.toString();
            }
        }
        catch (FileNotFoundException e) {
            Log.e("login activity", "File not found: " + e.toString());
        } catch (IOException e) {
            Log.e("login activity", "Can not read file: " + e.toString());
        }
        return ret;
    }

    private void writeToFile(String fileName, String data,Context context) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(context.openFileOutput(fileName, MODE_APPEND));
            outputStreamWriter.write(data);
            outputStreamWriter.close();
        }
        catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }


    @Override public void onConnectionSuspended(int i) {
        FileLogger.log("Location services connection suspended.", this.getApplicationContext());
    }

    @Override public void onConnectionFailed(ConnectionResult connectionResult) {
        FileLogger.log("Location services connection failed .", this.getApplicationContext());
    }

    @Override public void onLocationChanged(Location location) {
        FileLogger.log("Location changed.", this.getApplicationContext());
        if (location == null)
        {
            FileLogger.log("Location null ", this.getApplicationContext());
            return;
        }

        if (location.getAccuracy() > ApplicationConstants.MIN_ACCURACY_METRES ||
                System.currentTimeMillis() - location.getTime() >
                        ApplicationConstants.LOG_INTERVAL_MS) {
            FileLogger
                    .log("Location null/inaccurate/old (accuracy " + location.getAccuracy() + ") " +
                            location, this.getApplicationContext());
            //LocationLogger.log("FORCED UPLOAD CHECK", this.getApplicationContext());
        }
        else {
            try {
                handleNewLocation(location);
            } catch (JSONException e) {
                FileLogger.log("Error in onLocationChanged: " + e.getStackTrace().toString(),
                        this.getApplicationContext());
                e.printStackTrace();
            }
        }
    }

    public double getOffset(){
        TimeZone timezone = TimeZone.getDefault();
        int seconds = timezone.getOffset(Calendar.ZONE_OFFSET)/1000;
        double minutes = seconds/60;
        double hours = minutes/60;
        return hours;
    }


    /**************************************
     *  Methods for tracking acceleration
     **************************************/
    /*
    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {
        // do nothing
    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        if (event.sensor.getType() == Sensor.TYPE_ACCELEROMETER) {
            // grab the values and timestamp
            //FileLogger.log("Handling new acceleration.", this.getApplicationContext());
            addNewAccRecord(event);
        }
    }

    private void addNewAccRecord(SensorEvent event){
        xAxis.add(event.values[0]);
        yAxis.add(event.values[0]);
        zAxis.add(event.values[0]);
        timestamps.add(event.timestamp);
    }

    private String buildStringToLog() throws JSONException {
        JSONObject json = new JSONObject();
        json.put(ApplicationConstants.DEVICE_MODEL, ApplicationConstants.ANDROID);
        json.put(ApplicationConstants.TIMESTAMP, timestamps.get(0));
        json.put(ApplicationConstants.DEVICE_OPSYS, Build.VERSION.RELEASE);
        JSONObject acceleration = new JSONObject();
        acceleration.put(ApplicationConstants.TIMESTAMP, new JSONArray(timestamps));
        acceleration.put(ApplicationConstants.ACCELERATION_X, new JSONArray(xAxis));
        acceleration.put(ApplicationConstants.ACCELERATION_Y, new JSONArray(yAxis));
        acceleration.put(ApplicationConstants.ACCELERATION_Z, new JSONArray(zAxis));

        json.put(ApplicationConstants.ACCELERATION, acceleration);
        Log.d("MYINFO", "Acceleration stored: "+ json.toString());
        return json.toString() + "\n";
    }*/

}
