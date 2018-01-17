package uk.ac.cam.cl.loclogger.transfer;

import android.accounts.Account;
import android.content.AbstractThreadedSyncAdapter;
import android.content.ContentProviderClient;
import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.content.SyncResult;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.util.Log;
import android.os.Build;

import javax.net.ssl.HttpsURLConnection;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.FileInputStream;
import java.net.URL;
import java.io.DataOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.FileReader;
import org.json.JSONObject;
import java.io.ByteArrayOutputStream;

import java.util.zip.GZIPOutputStream;

import java.io.File;
import java.io.IOException;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.location.LocationTrackerActivity;
import uk.ac.cam.cl.loclogger.logging.FileLogger;

public class SyncAdapter extends AbstractThreadedSyncAdapter {

    public SyncAdapter(Context context, boolean autoInitialize) {
        super(context, autoInitialize);
    }

    public SyncAdapter(Context context, boolean autoInitialize, boolean allowParallelSyncs) {
        super(context, autoInitialize, allowParallelSyncs);
        FileLogger.log("Initialised sync adapter.", context);
        //Log.d("MYINFO","Initialised sync adapter.");

    }

    @Override
    public void onPerformSync(Account account, Bundle bundle, String s, ContentProviderClient
            contentProviderClient, SyncResult syncResult) {

        Context context = this.getContext();
        // If (time_since_last_upload >= 24 hours) -> upload. Otherwise, don't.
        if (System.currentTimeMillis() -  PreferenceManager.getDefaultSharedPreferences(context).getLong(ApplicationConstants.KEY_UPLOAD_TIME, 0L) >=
                (long)(3.9 * ApplicationConstants.UPLOAD_INTERVAL_MILLIS)) {

            // Get list of files available

            File directory = context.getFilesDir();
            File[] names = directory.listFiles();


            FileLogger.log("Syncing...", context);

            ConnectivityManager connMgr =
                    (ConnectivityManager) context.getSystemService(Context.CONNECTIVITY_SERVICE);
            NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
            if ((networkInfo != null) && (networkInfo.isConnected()) && (networkInfo.getType() == ConnectivityManager.TYPE_WIFI)) {  // check also if connected to WIFI here //) {
                try {
                    if (ApplicationConstants.DEBUG) {
                        // Log files
                        String file3 = FileLogger.filename + FileLogger.extension;
                        File file4 = new File(LocationTrackerActivity.getUserID(context) + '_' + FileLogger.filename + '_' +
                                System.currentTimeMillis() +
                                FileLogger.extension);
                        zip(file3, file4.getName() + ".zip", context);
                    }

                    for (File f : names) {
                        String name = f.getName();
                        if (!toSync(name, context)) {
                            continue; // Only sync the log file
                        }
                        pushFile(f, context);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }else{
            FileLogger.log("Less than 24 hours since last update... (no syncing yet).", context);
        }
    }


    private void pushFile(File file, Context context) throws IOException{

        HttpsURLConnection urlConnection;
        URL url;
        DataOutputStream dos;

        // open a URL connection to the Servlet
         url = new URL(ApplicationConstants.SERVER_URL);

        // Open a HTTP  connection to  the URL
        urlConnection = (HttpsURLConnection) url.openConnection() ;
        try {
            urlConnection.setRequestMethod("POST");
            urlConnection.setUseCaches(false); // don't use a cache copy
            urlConnection.setDoInput(true); // Allow Inputs
            urlConnection.setDoOutput(true); // Allow Outputs
            urlConnection.setRequestProperty("Authorization", "Bearer " + PreferenceManager.getDefaultSharedPreferences(context).getString(ApplicationConstants.ACCESS_TOKEN, null));
            urlConnection.setRequestProperty("Content-Type", "application/json");
            /*urlConnection.setRequestProperty("Content-Encoding", "gzip");  // UNCOMMENT FOR COMPRESSION
            urlConnection.setRequestProperty("Accept-Encoding", "gzip");*/  // UNCOMMENT FOR COMPRESSION

            // Build body to write
            //Read text from file
            StringBuffer objStr = new StringBuffer();

            try {
                BufferedReader br = new BufferedReader(new FileReader(file));
                String line;

                objStr.append("{\"" + ApplicationConstants.STUDY_ID + "\": 1, \"" +
                        ApplicationConstants.DEVICE_MODEL + "\": \"" + ApplicationConstants.ANDROID +"\", \"" +
                        ApplicationConstants.DEVICE_OPSYS + "\": \"" + Build.VERSION.RELEASE +"\", \"" +
                        "measurements\": ");


                objStr.append("[");
                if ((line = br.readLine()) != null) objStr.append(line);
                while ((line = br.readLine()) != null) {
                    objStr.append(", ");
                    objStr.append(line);
                }
                objStr.append("]");

                objStr.append("}");

                Log.d("MYINFO", "Data to submit:  "+objStr.toString());

                br.close();
            }
            catch (IOException e) {
                //You'll need to add proper error handling here
            }

            // COMPRESS OBJECT

            byte[] compressedData;
            compressedData = objStr.toString().getBytes(); // gzip(objStr.toString().getBytes()); // USE THE LATTER FOR COMPRESSION
            urlConnection.setRequestProperty("Content-Length", compressedData.length + "");

            //Log.d("MYINFO", "file to send " + file.getAbsolutePath());
            //Log.d("MYINFO", "data to send: " + compressedData);

            dos = new DataOutputStream(urlConnection.getOutputStream());
            dos.write(compressedData);

            // Responses from the server (message)
            if (urlConnection.getResponseCode() == HttpsURLConnection.HTTP_OK) {
                Log.d("MYINFO", "File "+file.getName()+" submitted correctly.");
                file.delete();
                setNewUploadTime(context);
            } else {
                if (urlConnection.getResponseCode() == HttpsURLConnection.HTTP_UNAUTHORIZED) {

                    // close the streams
                    dos.flush();
                    dos.close();

                    urlConnection.disconnect();

                    // REFRESH ACCESS TOKEN
                    Log.d("MYINFO", "ATTEMPT TO REFRESH TOKEN...");
                    refreshAccessToken(context);

                    // ATTEMPT TO SEND THE FILE AGAIN
                    Log.d("MYINFO", "ATTEMPT TO SEND FILE AGAIN...");
                    pushFile(file, context);
                }else{
                    Log.d("MYINFO", "HTTP CODE "+ urlConnection.getResponseCode() +" RECEIVED IN PUSH FILE.");
                }
            }

            // close the streams
            dos.flush();
            dos.close();

        }catch(Exception e){
            FileLogger.log("multipart post error " + e, context); // not sure if this is correct
        }finally {
            urlConnection.disconnect();
        }
    }

    private void refreshAccessToken(Context context) throws IOException{
        HttpsURLConnection urlConnection;
        URL url;
        DataOutputStream dos;
        String lineEnd = "\r\n";
        String twoHyphens = "--";
        String boundary = "*****";

        // open a URL connection to the Servlet
        url = new URL(ApplicationConstants.ACCESS_TOKEN_URL);
        // Open a HTTP  connection to  the URL
        urlConnection = (HttpsURLConnection) url.openConnection() ;
        try {
            urlConnection.setRequestMethod("POST");
            urlConnection.setUseCaches(false); // don't use a cache copy
            urlConnection.setDoInput(true); // Allow Inputs
            urlConnection.setDoOutput(true); // Allow Outputs
            urlConnection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary + "; charset=utf-8"); //, "application/json");

            // Build body to write (form)
            StringBuilder sb = new StringBuilder();
            sb.append(twoHyphens + boundary + lineEnd);
            sb.append("Content-Disposition: form-data; name=\"client_id\"" + lineEnd);
            sb.append(lineEnd);
            sb.append(ApplicationConstants.CLIENT_ID);
            sb.append(lineEnd);
            sb.append(twoHyphens + boundary + lineEnd);
            sb.append("Content-Disposition: form-data; name=\"client_secret\"" + lineEnd);
            sb.append(lineEnd);
            sb.append(ApplicationConstants.CLIENT_SECRET);
            sb.append(lineEnd);
            sb.append(twoHyphens + boundary + lineEnd);
            sb.append("Content-Disposition: form-data; name=\"refresh_token\"" + lineEnd);
            sb.append(lineEnd);
            sb.append(PreferenceManager.getDefaultSharedPreferences(context).getString(ApplicationConstants.REFRESH_TOKEN, null));
            sb.append(lineEnd);
            sb.append(twoHyphens + boundary + lineEnd);
            sb.append("Content-Disposition: form-data; name=\"grant_type\"" + lineEnd);
            sb.append(lineEnd);
            sb.append(ApplicationConstants.REFRESH_TOKEN);
            sb.append(lineEnd);
            sb.append(twoHyphens + boundary + twoHyphens + lineEnd);

            urlConnection.setRequestProperty("Content-Length", sb.toString().getBytes("UTF-8").length+"");
            //urlConnection.setRequestProperty("uploaded_file", name);

            // Log.d("MYINFO", sb.toString());

            dos = new DataOutputStream(urlConnection.getOutputStream());
            dos.writeBytes(sb.toString());

            // Responses from the server (message)
            if (urlConnection.getResponseCode() == HttpsURLConnection.HTTP_OK) {
                BufferedReader br = new BufferedReader(new InputStreamReader((urlConnection.getInputStream())));
                sb = new StringBuilder();
                String output;

                while ((output = br.readLine()) != null) {
                    sb.append(output);
                }
                // Parse received json
                JSONObject serverResponseMessage = new JSONObject(sb.toString());
                String access_token = serverResponseMessage.getString(ApplicationConstants.ACCESS_TOKEN);
                String refresh_token = serverResponseMessage.getString(ApplicationConstants.REFRESH_TOKEN);
                // Replace access token and refresh token
                SharedPreferences sPrefs = PreferenceManager.getDefaultSharedPreferences(this.getContext());
                Editor editor = sPrefs.edit();
                editor.putString(ApplicationConstants.ACCESS_TOKEN, access_token);
                editor.putString(ApplicationConstants.REFRESH_TOKEN, refresh_token);
                editor.commit();
                Log.d("MYINFO", "Refresh token received from Backend correctly");

            }else{
                Log.d("MYINFO", "response code received in refreshAuthToken: " + urlConnection.getResponseCode());
            }

            // close the streams
            dos.flush();
            dos.close();

        }catch(Exception e){
            FileLogger.log("multipart post error " + e, this.getContext()); // not sure if this is correct
        }finally {
            urlConnection.disconnect();
        }

    }

    private static byte[] gzip(byte[] input) throws IOException {
        GZIPOutputStream gzipOS = null;
        try {
            ByteArrayOutputStream byteArrayOS = new ByteArrayOutputStream();
            gzipOS = new GZIPOutputStream(byteArrayOS);
            gzipOS.write(input);
            gzipOS.flush();
            gzipOS.close();
            gzipOS = null;
            return byteArrayOS.toByteArray();
        } finally {
            if (gzipOS != null) {
                try { gzipOS.close(); } catch (Exception ignored) {}
            }
        }
    }

    private boolean toSync(String filename, Context context) {
        String user = LocationTrackerActivity.getUserID(context);
        //return filename.endsWith("zip");
        return (filename.endsWith("log") && !filename.startsWith("file"));
    }

    private static void setNewUploadTime(Context context) {
        SharedPreferences sPrefs = PreferenceManager.getDefaultSharedPreferences(context);
        Editor editor = sPrefs.edit();
        editor.putLong(ApplicationConstants.KEY_UPLOAD_TIME, System.currentTimeMillis());
        editor.commit();
    }

    private static void zip(String file, String zipFile, Context context) throws IOException {
        final int BUFFER_SIZE = 1024;
        BufferedInputStream origin;
        ZipOutputStream out = new ZipOutputStream(
                new BufferedOutputStream(context.openFileOutput(zipFile, Context.MODE_APPEND)));
        try {
            byte data[] = new byte[BUFFER_SIZE];
            FileInputStream fi = context.openFileInput(file);
            origin = new BufferedInputStream(fi, BUFFER_SIZE);
            try {
                ZipEntry entry = new ZipEntry(file.substring(file.lastIndexOf("/") + 1));
                out.putNextEntry(entry);
                int count;
                while ((count = origin.read(data, 0, BUFFER_SIZE)) != -1) {
                    out.write(data, 0, count);
                }
            } finally {
                origin.close();
            }
        } finally {
            out.close();
        }
    }

}