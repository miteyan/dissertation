//package uk.ac.cam.cl.loclogger.logging;
//
//import android.content.Context;
//
//import java.io.FileOutputStream;
//import java.io.IOException;
//
//import uk.ac.cam.cl.loclogger.location.LocationTrackerActivity;
//
//public class LocationLogger {
//
//    private static String filename = "location_log";
//    private static String extension = ".log";
//
//    public static synchronized void log(String s, Context context) {
//        FileOutputStream fos = null;
//        String user = LocationTrackerActivity.getUserID(context);
//        String file = user + filename + extension;
//        try {
//            fos = context.openFileOutput(file, Context.MODE_APPEND);
//            fos.write(s.getBytes());
//            FileLogger.log("Logging location: " + s, context);
//        } catch (IOException e) {
//            e.printStackTrace();
//        } finally {
//            try {
//                if (fos != null) {
//                    fos.close();
//                }
//            } catch (IOException e) {
//                e.printStackTrace();
//            }
//        }
//    }
//
//}