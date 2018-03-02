package uk.ac.cam.cl.loclogger.location;

import android.Manifest;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.Bundle;
import android.os.IBinder;
import android.support.v4.app.ActivityCompat;
import android.widget.Toast;

import com.commonsware.cwac.wakeful.WakefulIntentService;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.location.ActivityRecognition;
import com.google.android.gms.location.LocationListener;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationServices;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.alarms.ServiceAlarm;
import uk.ac.cam.cl.loclogger.logging.FileLogger;

public class LocationTrackerService extends WakefulIntentService implements
            GoogleApiClient.ConnectionCallbacks, GoogleApiClient.OnConnectionFailedListener,
            LocationListener {

    private final LocationRequest mLocationRequest;
    private GoogleApiClient mGoogleApiClient;
    public static boolean userActivity = true;

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
    }
//
//    public void handleNewLocation(Location location) throws JSONException {
//        FileLogger.log("Removing location updates.", this.getApplicationContext());
//        LocationServices.FusedLocationApi.removeLocationUpdates(mGoogleApiClient, this);
//        FileLogger.log("Handling new location.", this.getApplicationContext());
////        LocationLogger.log(buildStringToLog(location), this.getApplicationContext());
//    }

//    private String buildStringToLog(Location loc) throws JSONException {
//        JSONObject json = new JSONObject();
//        JSONObject timestamp = new JSONObject();
//        timestamp.put(ApplicationConstants.TIME, loc.getTime());
//        timestamp.put(ApplicationConstants.OFFSET, getOffset());
//        json.put(ApplicationConstants.TIMESTAMP, timestamp);
//        JSONObject location = new JSONObject();
//        location.put(ApplicationConstants.LOCATION_LATITUDE, loc.getLatitude());
//        location.put(ApplicationConstants.LOCATION_LONGITUDE, loc.getLongitude());
//        json.put(ApplicationConstants.LOCATION, location);
//        Log.d("MYINFO", "Location stored: "+ json.toString());
//        return json.toString() + "\n";
//    }

    @Override public void onConnected(Bundle bundle) {
        FileLogger.log("Services connected.", this.getApplicationContext());
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED && ActivityCompat
                .checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) !=
                PackageManager.PERMISSION_GRANTED) {
            return;
        }
        FileLogger.log("Getting location.", this.getApplicationContext());
        Location location = LocationServices.FusedLocationApi.getLastLocation(mGoogleApiClient);
        Context context = getApplicationContext();
//         Don't get a location if the user is still.
        if (!userActivity) {
            FileLogger.log("User is still. Do not get location.", getApplicationContext());
            SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.UK);
            Date now = new Date();
            String strDate = sdfDate.format(now);
            String row = strDate + "," + location.getLatitude() + "," + location.getLongitude() + "\t";
            String fileName = FileLogger.getFilename();
            FileLogger.writeToFile(fileName, row, context);
            return;
        }
        if (location == null) {
            FileLogger.log("Location null ", this.getApplicationContext());
            return;
        }
        CharSequence text = location.getLatitude() + " " + location.getLongitude();
        int duration = Toast.LENGTH_SHORT;
        Toast toast = Toast.makeText(context, text, duration);
        toast.show();

        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.UK);
        Date now = new Date();
        String strDate = sdfDate.format(now);
        String row = strDate + "," + location.getLatitude() + "," + location.getLongitude() + "\t";
        String fileName = FileLogger.getFilename();
        FileLogger.writeToFile(fileName, row, context);

        if (location.getAccuracy() > ApplicationConstants.MIN_ACCURACY_METRES ||
                System.currentTimeMillis() - location.getTime() >
                        ApplicationConstants.LOG_INTERVAL_MS) {
            FileLogger.log("Location inaccurate/old (accuracy " + location.getAccuracy() + ") " +
                    location, this.getApplicationContext());
            mLocationRequest.setExpirationDuration(ApplicationConstants.LOG_INTERVAL_MS);
            LocationServices.FusedLocationApi
                    .requestLocationUpdates(mGoogleApiClient, mLocationRequest, this);
        }
//        else {
//            try {
//                FileLogger.log("Suitable location.", this.getApplicationContext());
//                handleNewLocation(location);
//            } catch (JSONException e) {
//                e.printStackTrace();
//            }
//        }
    }

    @Override public void onConnectionSuspended(int i) {
        FileLogger.log("Location services connection suspended.", this.getApplicationContext());
    }

    @Override public void onConnectionFailed(ConnectionResult connectionResult) {
        FileLogger.log("Location services connection failed .", this.getApplicationContext());
    }

    @Override public void onLocationChanged(Location location) {
        FileLogger.log("Location changed.", this.getApplicationContext());
        if (location == null) {
            FileLogger.log("Location null ", this.getApplicationContext());
            return;
        }
        if (location.getAccuracy() > ApplicationConstants.MIN_ACCURACY_METRES ||
                System.currentTimeMillis() - location.getTime() >
                        ApplicationConstants.LOG_INTERVAL_MS) {
            FileLogger
                    .log("Location null/inaccurate/old (accuracy " + location.getAccuracy() + ") " +
                            location, this.getApplicationContext());
        }
//        else {
//            try {
//                handleNewLocation(location);
//            } catch (JSONException e) {
//                FileLogger.log("Error in onLocationChanged: " + e.getStackTrace().toString(),
//                        this.getApplicationContext());
//                e.printStackTrace();
//            }
//        }
    }
//    public double getOffset(){
//        TimeZone timezone = TimeZone.getDefault();
//        int seconds = timezone.getOffset(Calendar.ZONE_OFFSET)/1000;
//        double minutes = seconds/60;
//        double hours = minutes/60;
//        return hours;
//    }
}
