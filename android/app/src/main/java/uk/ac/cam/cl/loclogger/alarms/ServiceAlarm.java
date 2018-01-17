package uk.ac.cam.cl.loclogger.alarms;

import android.app.AlarmManager;
import android.app.AlarmManager.AlarmClockInfo;
import android.app.PendingIntent;
import android.content.Context;
import android.os.Build;

import com.commonsware.cwac.wakeful.WakefulIntentService;

import java.util.Calendar;

import uk.ac.cam.cl.loclogger.ApplicationConstants;
import uk.ac.cam.cl.loclogger.location.LocationTrackerService;
import uk.ac.cam.cl.loclogger.logging.FileLogger;

public class ServiceAlarm implements WakefulIntentService.AlarmListener {
    public ServiceAlarm() {

    }

    public void scheduleAlarms(AlarmManager alarmManager, PendingIntent pendingIntent, Context
            context) {

        // Datetime for alarm: LOG_INTERVAL_SECONDS from now
        Calendar calendar = Calendar.getInstance();
        calendar.setTimeInMillis(System.currentTimeMillis());
        calendar.add(Calendar.SECOND, ApplicationConstants.LOG_INTERVAL_SECONDS);


        // There is no AlarmClock (required to overcome limits on sampling frequency in sleep
        // mode) before Lollipop
        if (android.os.Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            AlarmClockInfo info = new AlarmClockInfo(calendar.getTimeInMillis(), pendingIntent);
            alarmManager.cancel(pendingIntent);
            alarmManager.setAlarmClock(info, pendingIntent);
            FileLogger.log("Scheduling alarm: " + calendar.getTime(), context);
        }

        // If we're not on Lollipop+ we just have to do the best we can. Sampling frequency may
        // not be great because there is a limit on how often a standard Alarm can wake the phone
        // from sleep.
        else {
            alarmManager.cancel(pendingIntent);
            alarmManager
                    .setExact(AlarmManager.RTC_WAKEUP, calendar.getTimeInMillis(), pendingIntent);
            FileLogger.log("Scheduling alarm: " + calendar.getTime(), context);
        }
    }

    @Override public void sendWakefulWork(Context context) {
        FileLogger.log("Sending work to IntentService.", context);
        WakefulIntentService.sendWakefulWork(context, LocationTrackerService.class);
    }

    @Override public long getMaxAge() {
        return ApplicationConstants.LOG_INTERVAL_MS;
    }
}