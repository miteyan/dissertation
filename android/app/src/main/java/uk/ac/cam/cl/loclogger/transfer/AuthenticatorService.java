package uk.ac.cam.cl.loclogger.transfer;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

public class AuthenticatorService extends Service {
    private Authenticator mAuthenticator;

    @Override public void onCreate() {
        mAuthenticator = new Authenticator(this);
    }

    @Override public IBinder onBind(Intent intent) {
        return mAuthenticator.getIBinder();
    }
}
