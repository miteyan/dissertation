package uk.ac.cam.cl.loclogger.logging;

import android.content.Context;

import java.io.FileOutputStream;
import java.io.IOException;

import uk.ac.cam.cl.loclogger.location.LocationTrackerActivity;

public class LocationLogger {

    public static String filename = "location_log";
    public static String extension = ".log";

    public static synchronized void log(String s, Context context) {
        FileOutputStream fos = null;
        String user = LocationTrackerActivity.getUserID(context);
        String file = user + filename + extension;
        try {
            fos = context.openFileOutput(file, Context.MODE_APPEND);
            fos.write(s.getBytes());
            FileLogger.log("Logging location: " + s, context);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (fos != null) {
                    fos.close();
                }

                // THIS PIECE CANNOT GO HERE!!!!! BECAUSE IF IT IS NOT LOCATION TO LOG, THEN THE SERVER WON'T TRY TO UPLOAD (EVEN THOUGH THERE ARE PREVIOUS LOCATIONS TO UPLOAD)

                // Try to upload, if it is time and we have WiFi
                /*if (System.currentTimeMillis() - getLastUploadTime(context) >
                        ApplicationConstants.UPLOAD_INTERVAL_MILLIS) {
                    Log.d("MYINFO", "Enough time has passed to try to upload.");
                    Calendar c = Calendar.getInstance();
                    int twoId = Integer.parseInt(PreferenceManager.getDefaultSharedPreferences(context).getString(ApplicationConstants.KEY_UUID, null).substring(4,6));
                    Log.d("MYINFO", "Enough time has passed to try to upload.");
                    if (((int)c.get(Calendar.HOUR_OF_DAY) == 15) &&
                            (((int)c.get(Calendar.MINUTE) == twoId)))  {
                        Log.d("MYINFO", "It's time to upload.");
                        Log.d("MYINFO", "Uploading data to server.");
                        tryToUpload(context, file);
                    } else {
                        Log.d("MYINFO", "It's not the hour to update yet.");
                    }
                } else {
                    Log.d("MYINFO", "It's not time to upload yet.");
                }*/

                ///////////////////


            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

}