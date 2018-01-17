package uk.ac.cam.cl.loclogger.startup;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

import uk.ac.cam.cl.loclogger.location.LocationTrackerActivity;
import uk.ac.cam.cl.loclogger.logging.FileLogger;

public class StartUpReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {
        if (intent.getAction().equals(Intent.ACTION_BOOT_COMPLETED)) {
            FileLogger.log("Received Intent: " + intent.getAction(), context);
            Intent i = new Intent(context, LocationTrackerActivity.class);
            i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            context.startActivity(i);
        }
    }
}
