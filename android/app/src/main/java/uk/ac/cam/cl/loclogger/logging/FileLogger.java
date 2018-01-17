package uk.ac.cam.cl.loclogger.logging;

import android.content.Context;
import android.util.Log;

import java.io.FileOutputStream;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.location.LocationTrackerActivity;

/*
    Log app info for debugging purposes.
 */
public class FileLogger {
    private static final String TAG = ApplicationConstants.TAG;
    public static String filename = "file_log";
    public static String extension = ".log";

    public static void log(String s, Context context) {
        Log.d(TAG, s);
        LocationTrackerActivity.appendToLogView(s);
        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date now = new Date();
        String strDate = sdfDate.format(now);
        String s2 = strDate + "\t" + s + "\n";
        if (ApplicationConstants.DEBUG) {
            FileOutputStream fos = null;
            String file = filename + extension;
            try {
                fos = context.openFileOutput(file, Context.MODE_APPEND);
                fos.write(s2.getBytes());
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    if (fos != null) {
                        fos.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}
