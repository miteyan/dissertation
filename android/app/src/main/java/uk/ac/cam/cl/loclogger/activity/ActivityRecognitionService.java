package uk.ac.cam.cl.loclogger.activity;

import android.app.IntentService;
import android.content.Intent;

import com.google.android.gms.location.ActivityRecognitionResult;
import com.google.android.gms.location.DetectedActivity;

import java.util.List;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.location.LocationTrackerService;
import uk.ac.cam.cl.loclogger.logging.FileLogger;

public class ActivityRecognitionService extends IntentService {

    public ActivityRecognitionService() {
        super(ActivityRecognitionService.class.getSimpleName());
    }

    public ActivityRecognitionService(String name) {
        super(name);
    }

    @Override protected void onHandleIntent(Intent intent) {
        if (ActivityRecognitionResult.hasResult(intent)) {
            ActivityRecognitionResult result = ActivityRecognitionResult.extractResult(intent);
            setUserActivity(userMayBeActive(result.getProbableActivities()));
        }
    }

    private void setUserActivity(boolean b) {
        FileLogger.log("User activity: " + b, this.getApplicationContext());
        LocationTrackerService.userActivity = b;
    }

    private boolean userMayBeActive(List<DetectedActivity> probableActivities) {
        for (DetectedActivity activity : probableActivities) {
            switch (activity.getType()) {
                case DetectedActivity.IN_VEHICLE: {
                    if (activity.getConfidence() >
                            ApplicationConstants.ACTIVITY_MOVING_CONFIDENCE) {
                        return true;
                    }
                    break;
                }
                case DetectedActivity.ON_BICYCLE: {
                    if (activity.getConfidence() >
                            ApplicationConstants.ACTIVITY_MOVING_CONFIDENCE) {
                        return true;
                    }
                    break;
                }
                case DetectedActivity.ON_FOOT: {
                    if (activity.getConfidence() >
                            ApplicationConstants.ACTIVITY_MOVING_CONFIDENCE) {
                        return true;
                    }
                    break;
                }
                case DetectedActivity.TILTING: {
                    if (activity.getConfidence() >
                            ApplicationConstants.ACTIVITY_MOVING_CONFIDENCE) {
                        return true;
                    }
                    break;
                }
                case DetectedActivity.UNKNOWN: {
                    if (activity.getConfidence() >
                            ApplicationConstants.ACTIVITY_MOVING_CONFIDENCE) {
                        return true;
                    }
                    break;
                }
            }
        }
        return false;
    }
}