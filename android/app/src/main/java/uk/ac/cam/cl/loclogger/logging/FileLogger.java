package uk.ac.cam.cl.loclogger.logging;

import android.content.Context;
import android.util.Log;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.location.LocationTrackerActivity;

import static android.content.Context.MODE_APPEND;

/*
    Log app info for debugging purposes.
 */
public class FileLogger {
    private static final String TAG = ApplicationConstants.TAG;
    public static String filename = "file_log";
    public static String extension = ".log";

    public static String getFilename() {
        Calendar calendar = new GregorianCalendar();
        Date trialTime = new Date();
        calendar.setTime(trialTime);
        System.out.println("Week number:" +
                calendar.get(Calendar.WEEK_OF_YEAR));
        return calendar.get(calendar.YEAR)+ "_" + calendar.get(Calendar.WEEK_OF_YEAR)+".loc";
    }

    public static String getLastFileName() {
        Calendar calendar = new GregorianCalendar();
        Date trialTime = new Date();
        calendar.setTime(trialTime);
        return calendar.get(calendar.YEAR)+ "_" + (calendar.get(Calendar.WEEK_OF_YEAR)-1)+".loc";
    }

    public static void log(String s, Context context) {
        Log.d(TAG, s);
//        LocationTrackerActivity.appendToLogView(s);
        SimpleDateFormat sdfDate = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date now = new Date();
        String strDate = sdfDate.format(now);
        String s2 = strDate + "\t" + s + "\n";
        if (ApplicationConstants.DEBUG) {
            FileOutputStream fos = null;
            String file = filename + extension;
            try {
                fos = context.openFileOutput(file, MODE_APPEND);
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
    public static String readFromFile(String fileName, Context context) {
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

    public static void writeToFile(String fileName, String data,Context context) {
        try {
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(context.openFileOutput(fileName, MODE_APPEND));
            outputStreamWriter.write(data);
            outputStreamWriter.close();
        }
        catch (IOException e) {
            Log.e("Exception", "File write failed: " + e.toString());
        }
    }
}
