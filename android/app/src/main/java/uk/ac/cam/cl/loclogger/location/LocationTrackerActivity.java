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
import android.content.res.AssetManager;
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
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.ObjectInputStream;
import java.net.URL;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Arrays;

import javax.net.ssl.HttpsURLConnection;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.R;
import uk.ac.cam.cl.loclogger.alarms.ServiceAlarm;
import uk.ac.cam.cl.loclogger.logging.FileLogger;
import uk.cam.ac.uk.mp781.clustering.Clustering;
import uk.cam.ac.uk.mp781.feature_extraction.FeatureExtraction;
import uk.cam.ac.uk.mp781.feature_extraction.Features;
import weka.classifiers.Classifier;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.SerializationHelper;

public class LocationTrackerActivity extends Activity {

    private TextView logview = null;

    public static String getUserID(Context context) {
        // Get ID for current user, required for file naming.
        SharedPreferences sPrefs = PreferenceManager.getDefaultSharedPreferences(context);
        return sPrefs.getString(ApplicationConstants.KEY_UUID, null);
    }

    @Override protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.locationtrackeractivity);
        Activity activity = this;
        // Check that we have permission to get location, if not, ask for permission.
        int permissionCheck =
                ContextCompat.checkSelfPermission(activity, Manifest.permission.ACCESS_FINE_LOCATION);
        if (permissionCheck != PermissionChecker.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(activity,
                    new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                    ApplicationConstants.LOCATION_PERMISSIONS_CODE);
        } else {
            // Start the location logging service.
            Log.d("MYINFO","onClick: Starting Service (we already have permission)");
            startService(activity.getApplicationContext());
        }
    }

    @Override protected void onResume() {
        super.onResume();
        setContentView(R.layout.locationtrackeractivity);

        Button thisWeekBtn = (Button)findViewById(R.id.graph_button);
        thisWeekBtn.setOnClickListener(v -> {
            String fileName = FileLogger.getFilename();
            getLabel(fileName);
        });

        Button lastWeekBtn = (Button) findViewById(R.id.button2);
        lastWeekBtn.setOnClickListener(view -> {
            String fileName = FileLogger.getLastFileName();
            getLabel(fileName);
        });
    }

    public void getLabel(String fileName) {
        try {
            Context context = getApplicationContext();
//            System.out.println(fileName);
            String locationAndTimes = FileLogger.readFromFile(fileName, context);
            String edgelist = Clustering.cluster(locationAndTimes, 5, 5);
            Features features = FeatureExtraction.getFeaturesFromEdgeList(edgelist);

            AssetManager assetManager = getAssets();
            Classifier cls = (Classifier) SerializationHelper.read(assetManager.open("forest.model"));
            Instance i = getInstanceFromFeature(features);
            double label = cls.classifyInstance(i);

            ScrollView scroller = new ScrollView(this);
            logview=new TextView(scroller.getContext());
            logview.setSingleLine(false);
            scroller.addView(logview);
            setContentView(scroller);
            String text = "Your movement patterns resemble a: ";
            if (label == 1) {
                text += "full-time worker";
            } else {
                text += "non full-time worker";
            }
            logview.setText(text);
        } catch (ArrayIndexOutOfBoundsException e) {
            ScrollView scroller = new ScrollView(this);
            logview=new TextView(scroller.getContext());
            logview.setSingleLine(false);
            scroller.addView(logview);
            setContentView(scroller);
            logview.setText("No data for last week. Try again later.");
        } catch (Exception e) {
            e.printStackTrace();
        }
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
//        FileLogger.log("Processing permissions...", this.getApplicationContext());
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == ApplicationConstants.LOCATION_PERMISSIONS_CODE) {
            // If request is cancelled, the result arrays are empty.
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
//                FileLogger.log("Starting service...", this.getApplicationContext());
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

    public static Instance getInstanceFromFeature(Features f) throws IOException {
        //Declaring attributes
        Attribute d1 = new Attribute("d1");
        Attribute d2 = new Attribute("d2");
        Attribute d3 = new Attribute("d3");
        Attribute d4 = new Attribute("d4");
        Attribute d5 = new Attribute("d5");
        Attribute d6 = new Attribute("d6");
        Attribute d7 = new Attribute("d7");
        Attribute d8 = new Attribute("d8");
        Attribute d9 = new Attribute("d9");
        Attribute d10 = new Attribute("d10");
        Attribute d11 = new Attribute("d11");
        Attribute d12 = new Attribute("d12");
        Attribute d13 = new Attribute("d13");
        Attribute d14 = new Attribute("d14");
        Attribute d15 = new Attribute("d15");
        Attribute d16 = new Attribute("d16");
        Attribute d17 = new Attribute("d17");
        Attribute d18 = new Attribute("d18");
        Attribute d19 = new Attribute("d19");
        Attribute d20 = new Attribute("d20");

        // Declare the class attribute along with its values contains two nominal values yes and no using FastVector. "ScheduledFirst" is the name of the class attribute
        FastVector fvClassVal = new FastVector(2);
        fvClassVal.addElement("1");
        fvClassVal.addElement("0");
        Attribute Class = new Attribute("ScheduledFirst", fvClassVal);

        // Declare the feature vector
        FastVector fvWekaAttributes = new FastVector(20);
        // Add attributes
        fvWekaAttributes.addElement(d1);
        fvWekaAttributes.addElement(d2);
        fvWekaAttributes.addElement(d3);
        fvWekaAttributes.addElement(d4);
        fvWekaAttributes.addElement(d5);
        fvWekaAttributes.addElement(d6);
        fvWekaAttributes.addElement(d7);
        fvWekaAttributes.addElement(d8);
        fvWekaAttributes.addElement(d9);
        fvWekaAttributes.addElement(d10);
        fvWekaAttributes.addElement(d11);
        fvWekaAttributes.addElement(d12);
        fvWekaAttributes.addElement(d13);
        fvWekaAttributes.addElement(d14);
        fvWekaAttributes.addElement(d15);
        fvWekaAttributes.addElement(d16);
        fvWekaAttributes.addElement(d17);
        fvWekaAttributes.addElement(d18);
        fvWekaAttributes.addElement(d19);
        fvWekaAttributes.addElement(d20);
        fvWekaAttributes.addElement(Class);
        Instances dataset = new Instances("graph_features", fvWekaAttributes, 0);
        //Creating a double array and defining values
        double[] attValues = new double[dataset.numAttributes()];
        attValues[0] = f.getNodes();
        attValues[1] = f.getEdges();
        attValues[2] = f.getMaxDegree();
        attValues[3] = f.getDensity();
        attValues[4] = f.getDiameter();
        attValues[5] = f.getRadius();
        attValues[6] = f.getCentreSize();
        attValues[7] = f.getMeanEccentricity();
        attValues[8] = f.getVarEccentricity();
        attValues[9] = f.getMeanClusteringCoefficient();
        attValues[10] = f.getVarClusteringCoefficient();
        attValues[11] = f.getMeanNodeBetweennessCentrality();
        attValues[12] = f.getVarNodeBetweennessCentrality();
        attValues[13] = f.getMeanShortestPathLength();
        attValues[14] = f.getVarShortestPathLength();
        attValues[15] = f.getMeanEdgeBetweenessCentrality();
        attValues[16] = f.getVarEdgeBetweenessCentrality();
        attValues[18] = f.getMeanPagerank();
        attValues[19] = f.getVarPagerank();
        //Create the new instance i1
        Instance i1 = new Instance(1.0, attValues);
        //Add the instance to the dataset (Instances) (first element 0)
        dataset.add(i1);
        //Define class attribute position
        dataset.setClassIndex(dataset.numAttributes()-1);
        return dataset.firstInstance();
    }
}
