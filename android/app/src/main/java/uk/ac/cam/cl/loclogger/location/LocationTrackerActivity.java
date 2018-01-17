package uk.ac.cam.cl.loclogger.location;

import android.Manifest;
import android.accounts.Account;
import android.accounts.AccountManager;
import android.app.Activity;
import android.content.ContentResolver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v4.content.PermissionChecker;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.RelativeLayout;
import android.widget.Toast;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.view.ViewGroup.LayoutParams;

import com.commonsware.cwac.wakeful.WakefulIntentService;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;

import javax.net.ssl.HttpsURLConnection;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.alarms.ServiceAlarm;
import uk.ac.cam.cl.loclogger.logging.FileLogger;


public class LocationTrackerActivity extends Activity {

    private static Activity activity;
    private static EditText userid_textfield;
    private static TextView logview = null;
    public static String inserted_userid=null;
    public static String received_passwd = null;


    // The authority for the sync adapter's (dummy) content provider
    public static final String AUTHORITY = "uk.ac.cam.cl.loclogger.provider";

    public static Account getUserAccount(Context context) {
        // Get the user account (required for sync, doesn't do anything else), or create
        // one if it doesn't exist.
        Account[] accounts = AccountManager.get(context).getAccountsByType(ApplicationConstants.ACCOUNT_TYPE);
        if (accounts.length < 1) {
            return createSyncAccount(context);
        }
        else {
            return accounts[0]; // Should only be one account.
        }
    }

    public static String getUserID(Context context) {
        // Get ID for current user, required for file naming.
        SharedPreferences sPrefs = PreferenceManager.getDefaultSharedPreferences(context);
        return sPrefs.getString(ApplicationConstants.KEY_UUID, null);
    }

    public static void appendToLogView(final String text) {
        if (logview != null)
        {
            activity.runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    // This code will always run on the UI thread, therefore is safe to modify UI elements.
                    logview.append(text+"\n");
                }
            });
        }
        return;
    }

    public static Account createSyncAccount(Context context) {
        Account newAccount = new Account(inserted_userid, ApplicationConstants.ACCOUNT_TYPE);
        AccountManager accountManager = (AccountManager) context.getSystemService(ACCOUNT_SERVICE);
        boolean success = accountManager.addAccountExplicitly(newAccount, received_passwd, null);
        if (success) {
            // Inform the system that this account supports sync
            ContentResolver.setIsSyncable(newAccount, AUTHORITY, 1);
            // Inform the system that this account is eligible for auto sync  (NEW CODE)
            ContentResolver.setSyncAutomatically(newAccount, AUTHORITY, true);
            // Recommend a schedule for auto sync
            Bundle bundle = new Bundle();
            //bundle.putBoolean(ContentResolver.SYNC_EXTRAS_MANUAL, true);
            //bundle.putBoolean(ContentResolver.SYNC_EXTRAS_EXPEDITED, true);
            FileLogger.log("Set up sync requests.", context);
            ContentResolver.addPeriodicSync(
                    newAccount,
                    AUTHORITY,
                    bundle,
                    ApplicationConstants.UPLOAD_INTERVAL_SECONDS);

            return newAccount;
        }
        else {
            return null;
        }
    }

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
         activity = this;
        Log.d("MYINFO","Loading my layout");
        LinearLayout linLayout = new LinearLayout(this);
        linLayout.setOrientation(LinearLayout.VERTICAL);
        linLayout.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));
        assert linLayout != null;

        // Delete previous files location
        File directory = activity.getFilesDir();
        File[] files = directory.listFiles();
        for (File f:files){
            if (f.getName().endsWith("log") && !f.getName().startsWith("file")){
                f.delete();
                Log.d("MYINFO","onClick: old location logs deleted");
            }

        }

        TextView textv = new TextView(this);
        textv.setTextSize(20);
        textv.setPadding(15,15,15,15);
        textv.setText("Please insert your 6-digit ID:");
        textv.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));

        userid_textfield = new EditText(this);
        userid_textfield.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.WRAP_CONTENT));

        Button btn = new Button(this);
        btn.setText("Login");
        btn.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));

        btn.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String regex = "\\d{6}";
                inserted_userid = userid_textfield.getText().toString();
                if(!inserted_userid.matches(regex)) {
                    Toast.makeText(activity, "Insert your 6-digit ID number.", Toast.LENGTH_LONG).show();
                    return;
                }

                Log.d("MYINFO", "USER ID:" + inserted_userid);
                if (getUserAccount(activity) == null) {
                    FileLogger.log("Couldn't create user account.", activity);
                    activity.finish();
                }

                // Create user in backend and get initial access token
                // Log.d("MYINFO", "HERE");
                new CreateAppUserTask(activity).execute(inserted_userid);
                new RetrieveAuthTokensTask(activity).execute(inserted_userid);

                // Check that we have permission to get location, if not, ask for permission.
                int permissionCheck =
                        ContextCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_FINE_LOCATION);
                if (permissionCheck != PermissionChecker.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(activity,
                            new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                            ApplicationConstants.LOCATION_PERMISSIONS_CODE);
                }
                else {
                    CharSequence text = "installed correctly";
                    int duration = Toast.LENGTH_SHORT;
                    Toast toast = Toast.makeText(activity, text, duration);
                    toast.show();
                    // Start the location logging service.
                    Log.d("MYINFO","onClick: Starting Service (we already have permission)");
                    startService(activity.getApplicationContext());
                    activity.finish();
                }

            }
        });
        linLayout.addView(textv);
        linLayout.addView(userid_textfield);
        linLayout.addView(btn);

        inserted_userid = getUserID(this.getApplicationContext());
        if (inserted_userid == null) {
            setContentView(linLayout);
        }
        else
        {
            if (getUserAccount(activity) == null) {
                FileLogger.log("Couldn't create user account.", activity);
                activity.finish();
            }
        }
    }

    @Override protected void onResume() {
        super.onResume();
        if (inserted_userid == null) {
            Toast.makeText(this, "Configuring user account...", Toast.LENGTH_SHORT).show();

        }
        else{
            Toast.makeText(this,  "Location logging is active.", Toast.LENGTH_SHORT).show();

            RelativeLayout layout = new RelativeLayout(this);

            Button b = new Button(layout.getContext());
            b.setText("Button");
            layout.addView(b);
            System.out.println("Button added");

//            FrameLayout frameLayout = new FrameLayout(this);
//            ScrollView scroller = new ScrollView(this);

//            Button graphButton = new Button(this);
//            graphButton.setText("Construct graph");
//            graphButton.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
//
//            graphButton.setOnClickListener(v -> {
                // Code here executes on main thread after user presses button
//                Toast.makeText(this, "Graph", Toast.LENGTH_LONG).show();
//
//            });
//            frameLayout.addView(graphButton);
//            frameLayout.addView(scroller);

//            logview=new TextView(this);
//            logview.setSingleLine(false);
//            scroller.addView(logview);
//            setContentView(scroller);
//            logview.setText("User ID: " + inserted_userid + "\n");


        }
        Log.d("MYINFO","onResume Called");

    }

    @Override protected void onPause() {
        super.onPause();
        Log.d("MYINFO","onPause Called");
    }

    @Override protected void onStart() {
        super.onStart();
        Log.d("MYINFO","onStart Called");

    }

    @Override public void onRequestPermissionsResult(int requestCode,
                                                     @NonNull String permissions[],
                                                     @NonNull int[] grantResults) {
        FileLogger.log("Processing permissions...", this.getApplicationContext());
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == ApplicationConstants.LOCATION_PERMISSIONS_CODE) {
            // If request is cancelled, the result arrays are empty.
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                FileLogger.log("Starting service...", this.getApplicationContext());
                Log.d("MYINFO","onRequestPermissionsResult: Starting Service");
                startService(getApplicationContext());
            }
        }
        this.finish();
    }

    private void startService(final Context context) {
        AsyncTask.execute(new Runnable() {
            @Override public void run() {
                setAlarm(context);
            }
        });
        Intent mServiceIntent = new Intent(this, LocationTrackerService.class);
        WakefulIntentService.sendWakefulWork(context, mServiceIntent);

        CharSequence text = "Successfully installed! \n Location logging now active";
        int duration = Toast.LENGTH_LONG;
        Toast toast = Toast.makeText(context, text, duration);
        toast.show();

    }

    private void setAlarm(Context context) {
        ServiceAlarm alarm = new ServiceAlarm();
        LocationTrackerService.scheduleAlarms(alarm, context);

    }

    private class CreateAppUserTask extends AsyncTask<String, Void, String> {

        private Context context;

        private CreateAppUserTask(Context context) {
            this.context = context;
        }

        @Override
        protected String doInBackground(String... params) {
            // username, email, password
            try {
                HttpsURLConnection urlConnection = null;
                URL url = null;
                DataOutputStream dos = null;

                // open a URL connection to the Servlet
                url = new URL(ApplicationConstants.AUTHORIZATION_URL);
                // Open a HTTP  connection to  the URL
                urlConnection = (HttpsURLConnection) url.openConnection();

                try {
                    urlConnection.setRequestMethod("POST");
                    urlConnection.setUseCaches(false); // don't use a cache copy
                    urlConnection.setDoInput(true); // Allow Inputs
                    urlConnection.setDoOutput(true); // Allow Outputs
                    urlConnection.setRequestProperty("Content-Type", "application/json");
                    // Build body to write (form)
                    JSONObject obj = new JSONObject();
                    obj.put("username", params[0]);
                    obj.put("email", ApplicationConstants.APP_EMAIL);
                    obj.put("password", ApplicationConstants.APP_PASSWORD);
                    String objStr = obj.toString();
                    //Log.d("MYINFO", "OBJECT TO SEND:");
                    //Log.d("MYINFO", obj.toString());


                    urlConnection.setRequestProperty("Content-Length", objStr.getBytes("UTF-8").length + "");
                     dos = new DataOutputStream(urlConnection.getOutputStream());
                    dos.writeBytes(objStr.toString());

                    // Responses from the server (message)
                    if (urlConnection.getResponseCode() == HttpsURLConnection.HTTP_OK) {
                        Log.d("MYINFO", "User registered in the backend correctly.");

                        // Parse received json
                        BufferedReader br = new BufferedReader(new InputStreamReader((urlConnection.getInputStream())));
                        StringBuilder sb = new StringBuilder();
                        String output;

                        while ((output = br.readLine()) != null) {
                            sb.append(output);
                        }
                        //Log.d("MYINFO", "output received when creating user: " + sb.toString());
                        JSONObject serverResponseMessage = new JSONObject(sb.toString());
                        received_passwd = serverResponseMessage.getString(ApplicationConstants.PASSWD);

                        SharedPreferences sPrefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                        SharedPreferences.Editor editor = sPrefs.edit();
                        editor.putString(ApplicationConstants.KEY_UUID, inserted_userid);
                        editor.putString(ApplicationConstants.PASSWD, received_passwd);
                        editor.commit();
                        //Log.d("MYINFO", "received passwd: " + received_passwd);
                    } else {
                        Log.d("MYINFO", "response code received in createAppUserTask: " + urlConnection.getResponseCode());
                    }
                    // close the streams
                    dos.flush();
                    dos.close();

                } catch (Exception e) {
                    FileLogger.log("multipart post error " + e, context); // not sure if this is correct
                } finally {
                    urlConnection.disconnect();
                }
            } catch (IOException e) {
                FileLogger.log("IOException " + e, context);
            }
            return null;
        }

    }

    private class RetrieveAuthTokensTask extends AsyncTask<String, Void, String> {

        private Context context;

        private RetrieveAuthTokensTask(Context context) {
            this.context = context;
        }

        @Override
        protected String doInBackground(String... params) {
            try {
                HttpsURLConnection urlConnection;
                URL url;
                DataOutputStream dos;
                String lineEnd = "\r\n";
                String twoHyphens = "--";
                String boundary = "*****";

                // open a URL connection to the Servlet
                url = new URL(ApplicationConstants.ACCESS_TOKEN_URL);
                // Open a HTTP  connection to  the URL
                urlConnection = (HttpsURLConnection) url.openConnection();
                try {
                    urlConnection.setRequestMethod("POST");
                    urlConnection.setUseCaches(false); // don't use a cache copy
                    urlConnection.setDoInput(true); // Allow Inputs
                    urlConnection.setDoOutput(true); // Allow Outputs
                    urlConnection.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary + "; charset=utf-8"); //, "application/json");

                    // Build body to write (form)
                    StringBuilder sb = new StringBuilder();
                    sb.append(twoHyphens + boundary + lineEnd);
                    sb.append("Content-Disposition: form-data; name=\"username\"" + lineEnd);
                    sb.append(lineEnd);
                    sb.append(params[0]);
                    sb.append(lineEnd);
                    sb.append(twoHyphens + boundary + lineEnd);
                    sb.append("Content-Disposition: form-data; name=\"password\"" + lineEnd);
                    sb.append(lineEnd);
                    //sb.append(params[1]);
                    sb.append(PreferenceManager.getDefaultSharedPreferences(context).getString(ApplicationConstants.PASSWD, null));
                    sb.append(lineEnd);
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
                    sb.append("Content-Disposition: form-data; name=\"grant_type\"" + lineEnd);
                    sb.append(lineEnd);
                    sb.append(ApplicationConstants.GRANT_TYPE);
                    sb.append(lineEnd);
                    sb.append(twoHyphens + boundary + twoHyphens + lineEnd);

                    //Log.d("MYINFO", "Body query to send: "+sb.toString());

                    urlConnection.setRequestProperty("Content-Length", sb.toString().getBytes("UTF-8").length + "");
                    //urlConnection.setRequestProperty("uploaded_file", name);

                    dos = new DataOutputStream(urlConnection.getOutputStream());
                    dos.writeBytes(sb.toString());

                    // Responses from the server (message)
                    if (urlConnection.getResponseCode() == HttpsURLConnection.HTTP_OK) {
                        // Parse received json
                        BufferedReader br = new BufferedReader(new InputStreamReader((urlConnection.getInputStream())));
                        sb = new StringBuilder();
                        String output;

                        while ((output = br.readLine()) != null) {
                            sb.append(output);
                        }
                        JSONObject serverResponseMessage = new JSONObject(sb.toString());
                        String access_token = serverResponseMessage.getString(ApplicationConstants.ACCESS_TOKEN);
                        String refresh_token = serverResponseMessage.getString(ApplicationConstants.REFRESH_TOKEN);
                        // Replace access token and refresh token
                        SharedPreferences sPrefs = PreferenceManager.getDefaultSharedPreferences(getApplicationContext());
                        SharedPreferences.Editor editor = sPrefs.edit();
                        editor.putString(ApplicationConstants.ACCESS_TOKEN, access_token);
                        editor.putString(ApplicationConstants.REFRESH_TOKEN, refresh_token);
                        editor.commit();

                        Log.d("MYINFO", "Oauth token received from Backend correctly");
                        Log.d("MYINFO", "Access_token: "+access_token);
                        Log.d("MYINFO", "Refresh_token: "+refresh_token);

                    }else{
                        Log.d("MYINFO", "response code received in reqAuthToken: " + urlConnection.getResponseCode());
                    }

                    // close the streams
                    dos.flush();
                    dos.close();

                } catch (Exception e) {
                    FileLogger.log("multipart post error " + e, context); // not sure if this is correct
                } finally {
                    urlConnection.disconnect();
                }
            } catch (IOException e) {
                FileLogger.log("IOException " + e, context);
            }
            return null;
        }
    }


}



